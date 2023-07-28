from utils.constants import SLACK, CONFLUENCE

SLACK_BOT_TOKEN = "slack_bot_token"
SLACK_CLIENT_ID = "slack_client_id"
SLACK_CLIENT_SIGNATURE = "slack_client_signature"
SLACK_APP_TOKEN = "slack_app_token"

CONFLUENCE_API_KEY = "confluence_api_key"
CONFLUENCE_EMAIL_ID = "confluence_email_id"

FETCHER_CONFIG_VALUES = {

    SLACK: {
        "display_name": "Slack",
        "configs": [{"name": SLACK_BOT_TOKEN, "display_name": "Bot Token"},
                    {"name": SLACK_CLIENT_ID, "display_name": "Client ID"},
                    {"name": SLACK_CLIENT_SIGNATURE, "display_name": "Client Signature"},
                    {"name": SLACK_APP_TOKEN, "display_name": "App Token"}],
        "help_url": "https://github.com/unifyiq/unifyiq/tree/src-config-to-db/unifyiq/fetchers#slack"},
    CONFLUENCE: {
        "display_name": "Confluence",
        "configs": [{"name": CONFLUENCE_API_KEY, "display_name": "Api Key"},
                    {"name": CONFLUENCE_EMAIL_ID, "display_name": "Email ID"}],
        "help_url": "https://github.com/unifyiq/unifyiq/tree/src-config-to-db/unifyiq/fetchers#confluence-wiki"}
}
