from tradestation_python import cli


def test_cli_template():
    assert cli.cli() is None
