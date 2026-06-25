from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Gmail Read-Only scope
# SCOPES = [
#     "https://www.googleapis.com/auth/gmail.readonly"
# ]
SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send"
]

CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"


def get_credentials():
    """
    Authenticate the user and return valid Gmail credentials.
    """

    creds = None

    # Load existing token if available
    if Path(TOKEN_FILE).exists():
        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    # If credentials are missing or invalid
    if not creds or not creds.valid:

        # Refresh expired token
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            # First-time login
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        # Save token for future runs
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return creds