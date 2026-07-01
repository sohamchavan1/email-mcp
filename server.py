from mcp.server.fastmcp import FastMCP

from gmail_service import GmailService
from llm_service import LLMService


# Create MCP Server
mcp = FastMCP("Email Assistant")


# -------------------------
# Gmail Service Singleton
# -------------------------

gmail_service = None


def get_gmail_service():

    global gmail_service

    if gmail_service is None:
        gmail_service = GmailService()

    return gmail_service


# -------------------------
# LLM Service Singleton
# -------------------------

llm_service = None


def get_llm_service():

    global llm_service

    if llm_service is None:
        llm_service = LLMService()

    return llm_service


# -------------------------
# Tools
# -------------------------

@mcp.tool()
def list_recent_emails(limit: int = 5) -> list[dict]:
    """
    Fetch recent emails.
    """

    return get_gmail_service().get_recent_emails(limit)


@mcp.tool()
def search_emails(
    query: str,
    limit: int = 5
) -> list[dict]:
    """
    Search Gmail using Gmail search syntax.

    Examples:
    - interview
    - from:amazon
    - subject:meeting
    - label:unread
    - newer_than:7d
    """

    return get_gmail_service().search_emails(
        query,
        limit
    )


@mcp.tool()
def read_email(message_id: str) -> dict:
    """
    Read full email contents.
    """

    return get_gmail_service().read_email(
        message_id
    )


@mcp.tool()
def send_email(
    to: str,
    subject: str,
    body: str
) -> dict:
    """
    Send an email.
    """

    return get_gmail_service().send_email(
        to,
        subject,
        body
    )


@mcp.tool()
def summarize_email(
    message_id: str
) -> dict:
    """
    Read an email and summarize it using local Qwen 3.5.
    """

    email = (
        get_gmail_service()
        .read_email(message_id)
    )

    summary = (
        get_llm_service()
        .summarize_email(
            email["body"]
        )
    )
    

    return {
        "message_id": message_id,
        "subject": email["subject"],
        "from": email["from"],
        "summary": summary
    }


# -------------------------
# Run MCP Server
# -------------------------

if __name__ == "__main__":
    mcp.run(
        transport="stdio"
    )