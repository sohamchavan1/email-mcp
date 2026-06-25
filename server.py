from mcp.server.fastmcp import FastMCP

from gmail_service import GmailService

# Create the MCP server
mcp = FastMCP("Email Assistant")

# Create Gmail service instance
# gmail_service = GmailService()
gmail_service = None
def get_gmail_service():
    global gmail_service

    if gmail_service is None:
        gmail_service = GmailService()

    return gmail_service


@mcp.tool()
def list_recent_emails(limit: int = 5) -> list[dict]:
    return get_gmail_service().get_recent_emails(limit)

@mcp.tool()
def search_emails(query: str, limit: int = 5) -> list[dict]:
    """
    Search Gmail using Gmail search syntax.

    Examples:
    - interview
    - from:amazon
    - subject:meeting
    - label:unread
    - newer_than:7d
    """

    return get_gmail_service().search_emails(query, limit)

@mcp.tool()
def send_email(
    to: str,
    subject: str,
    body: str
) -> dict:
    """
    Send an email.

    Args:
        to: Recipient email address.
        subject: Email subject.
        body: Email body.
    """

    return get_gmail_service().send_email(
        to,
        subject,
        body
    )

@mcp.tool()
def read_email(message_id: str) -> dict:
    return get_gmail_service().read_email(message_id)


if __name__ == "__main__":
    mcp.run(transport="stdio")