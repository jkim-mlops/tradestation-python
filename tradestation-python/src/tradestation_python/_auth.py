import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from time import time
from typing import Dict, Generator, List, Optional
from webbrowser import open_new

from httpx import Auth, Request
from httpx._models import Response
from pydantic import HttpUrl

from ._base_client import SyncAuthClient
from ._config import AuthSettings
from .types.enums.scope import Scope
from .types.responses import TokenInfo
from .types.responses.token import TokenInfoWithRefresh


class AuthHTTPServer(HTTPServer):
    received_params: Dict[str, str]

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        super().__init__(*args, **kwargs)
        self.received_params = {}


class ParamsHandler(BaseHTTPRequestHandler):
    sever: AuthHTTPServer

    def do_GET(self) -> None:
        # Enusre proper type with parameter handling.
        if not isinstance(self.server, AuthHTTPServer):
            raise TypeError("Server must be of type `AuthHTTPServer`.")

        # Parse query parameters.
        parsed_path = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed_path.query)
        self.server.received_params = {k: v[0] for k, v in params.items()}  # flatten

        # Respond to client.
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        html_response = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Authorization Complete</title>
        </head>
        <body>
            <h2>Authorization successful!</h2>
            <p>Parameters received. This window will close automatically...</p>
            <script>
                // Close the window after a short delay
                setTimeout(function() {
                    window.close();
                }, 2000);
                
                // Fallback: try to close immediately for popup windows
                if (window.opener) {
                    window.close();
                }
            </script>
        </body>
        </html>
        """
        self.wfile.write(html_response.encode("utf-8"))

        # Shut down the server in a background thread to avoid blocking.
        threading.Thread(target=self.server.shutdown).start()

    def log_message(self, format: str, *args) -> None:  # noqa: ANN002
        pass


class OAuth2PasswordBearer(SyncAuthClient):
    def __init__(
        self,
        base_url: Optional[str] = None,
        audience: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        response_type: Optional[str] = None,
        state: Optional[str] = None,
        scopes: Optional[List[Scope]] = None,
        timeout: Optional[float] = None,
        retries: Optional[int] = None,
    ) -> None:
        self.settings = AuthSettings()
        if base_url is None:
            base_url = self.settings.base_url
        if audience is None:
            audience = self.settings.audience
        if client_id is None:
            client_id = self.settings.client_id
        if client_id is None:
            raise ValueError(
                "The client_id must be set either through the client client_id parameter "
                "or the TS_AUTH_CLIENT_ID environment variable."
            )
        if client_secret is None:
            client_secret = self.settings.client_secret
        if client_secret is None:
            raise ValueError(
                "The client_secret must be set either throught the client client_secret parameter"
                "or the TS_AUTH_CLIENT_SECRET environment variable."
            )
        if redirect_uri is None:
            redirect_uri = self.settings.redirect_uri
        if response_type is None:
            response_type = "code"
        if state is None:
            state = self.settings.state
        if timeout is None:
            timeout = self.settings.timeout
        if retries is None:
            retries = self.settings.retries
        if scopes is None:
            scopes = [
                Scope.OPENID,
                Scope.PROFILE,
                Scope.OFFLINE_ACCESS,
                Scope.MARKET_DATA,
                Scope.READ_ACCOUNT,
            ]

        super().__init__(
            base_url=base_url,
            audience=audience,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            response_type=response_type,
            state=state,
            scopes=scopes,
            timeout=timeout,
            retries=retries,
        )

        self.refresh_token = self.settings.refresh_token

    def _get_code(self) -> str:
        # Start authentication flow in a new window.
        scope = " ".join([scope.value for scope in self.scopes])
        auth_url = (
            f"{self.settings.openid.authorization_endpoint}"
            f"?response_type={self.response_type}"
            f"&client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
            f"&audience={self.audience}"
            f"&state={self.state}"
            f"&scope={scope}"
        )
        open_new(auth_url)

        # Extract host and port from redirect_uri, provide defaults if missing.
        redirect = HttpUrl(self.redirect_uri)
        host = redirect.host if redirect.host else "127.0.0.1"
        port = redirect.port if redirect.port else 8080
        httpd = AuthHTTPServer((host, port), ParamsHandler)
        httpd.serve_forever()

        # Set code with error handling.
        if not httpd.received_params or (
            "code" not in httpd.received_params or "state" not in httpd.received_params
        ):
            raise ValueError(
                "Received params from auth redirect are invalid. Authorization failed!"
            )
        elif httpd.received_params["state"] != self.state:
            raise Exception(
                "Redirect state param does not match expected state. Potential bad actor intercepting credentials!"
            )
        else:
            return httpd.received_params["code"]

    def get_token_info(self) -> TokenInfo:
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        headers = {"content-type": "application/x-www-form-urlencoded"}
        info = None
        if not self.refresh_token:
            code = self._get_code()
            data["code"] = code
            data["grant_type"] = "authorization_code"
            data["redirect_uri"] = self.redirect_uri
            info = self._make_request(
                method="POST",
                url=self.settings.openid.token_endpoint,
                response_model=TokenInfoWithRefresh,
                headers=headers,
                data=data,
            )
            self.refresh_token = info.refresh_token
        else:
            data["grant_type"] = "refresh_token"
            data["refresh_token"] = self.refresh_token
            info = self._make_request(
                method="POST",
                url=self.settings.openid.token_endpoint,
                response_model=TokenInfo,
                headers=headers,
                data=data,
            )
        return info


class TradeStationAuth(Auth):
    _token_info: Optional[TokenInfo]

    def __init__(
        self, oauth_client: Optional[OAuth2PasswordBearer] = None, buffer_seconds: int = 180
    ) -> None:
        self.oauth_client = oauth_client or OAuth2PasswordBearer()
        self.buffer_seconds = buffer_seconds
        self._token_info = None

    def sync_auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        if (
            self._token_info is None
            or int(time()) >= self._token_info.expires_at + self.buffer_seconds
        ):
            self._token_info = self.oauth_client.get_token_info()
        request.headers["Authorization"] = f"Bearer {self._token_info.access_token}"
        yield request
