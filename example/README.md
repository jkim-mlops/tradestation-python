# Example

1. At a minimum, you need the client id and client secret environment variables set. I recommend you store the credentials in a `.env` file.

    ```
    TS_AUTH_CLIENT_ID=<your-client-id>
    TS_AUTH_CLIENT_SECRET=<your-client-secret>
    ```

1. Once set, you can simply initialize the client and access the API endpoints as shown below. When the code runs, you will be redirected to TradeStation's sign in page where you can authenticate your account.

    ```python
    ts = TradeStation()
    bars = ts.market_data.bars("SMCI", barsback=14)
    print(bars)
    ```

1. To avoid having to re-authenticate every time the script runs, you can access the refresh token and set it as `TS_AUTH_REFRESH_TOKEN` in your `.env` file.

    ```python
    ts = TradeStation()
    print(ts.auth.oauth_client.refresh_token)
    ```

    ```
    TS_AUTH_CLIENT_ID=<your-client-id>
    TS_AUTH_CLIENT_SECRET=<your-client-secret>
    TS_AUTH_REFRESH_TOKEN=<your-refresh-token>
    ```