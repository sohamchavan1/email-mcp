from typing import List, Dict
import base64
from email.message import EmailMessage

from bs4 import BeautifulSoup
from googleapiclient.discovery import build

from auth import get_credentials


class GmailService:

    def __init__(self):
        creds = get_credentials()
        self.service = build(
            "gmail",
            "v1",
            credentials=creds
        )

    def get_recent_emails(self, limit: int = 5) -> List[Dict]:
        """
        Fetch the latest emails.
        """

        try:

            results = (
                self.service.users()
                .messages()
                .list(
                    userId="me",
                    maxResults=limit
                )
                .execute()
            )

            messages = results.get("messages", [])

            emails = []

            for msg in messages:
                emails.append(
                    self.get_email_details(msg["id"])
                )

            return emails

        except Exception as e:
            raise RuntimeError(f"Failed to fetch recent emails: {e}")

    def search_emails(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Search Gmail using Gmail search syntax.
        """

        try:

            results = (
                self.service.users()
                .messages()
                .list(
                    userId="me",
                    q=query,
                    maxResults=limit
                )
                .execute()
            )

            messages = results.get("messages", [])

            emails = []

            for msg in messages:
                emails.append(
                    self.get_email_details(msg["id"])
                )

            # return emails
            if not emails:
                return [{
                    "message": f"No emails found matching '{query}'."
                }]

            return emails

        except Exception as e:
            raise RuntimeError(f"Failed to search emails: {e}")

    def get_email_details(self, message_id: str) -> Dict:
        """
        Fetch basic details of a single email.
        """

        try:

            message = (
                self.service.users()
                .messages()
                .get(
                    userId="me",
                    id=message_id
                )
                .execute()
            )

            headers = message["payload"]["headers"]

            subject = ""
            sender = ""
            date = ""

            for header in headers:

                if header["name"] == "Subject":
                    subject = header["value"]

                elif header["name"] == "From":
                    sender = header["value"]

                elif header["name"] == "Date":
                    date = header["value"]

            return {
                "id": message_id,
                "subject": subject,
                "from": sender,
                "date": date
            }

        except Exception as e:
            raise RuntimeError(f"Failed to fetch email details: {e}")

    def read_email(self, message_id: str) -> Dict:
        """
        Read complete email including body.
        """

        try:

            message = (
                self.service.users()
                .messages()
                .get(
                    userId="me",
                    id=message_id,
                    format="full"
                )
                .execute()
            )

            headers = message["payload"]["headers"]

            subject = ""
            sender = ""
            date = ""

            for header in headers:

                if header["name"] == "Subject":
                    subject = header["value"]

                elif header["name"] == "From":
                    sender = header["value"]

                elif header["name"] == "Date":
                    date = header["value"]

            body = self._extract_body(message["payload"])

            return {
                "id": message_id,
                "subject": subject,
                "from": sender,
                "date": date,
                "body": body
            }

        except Exception as e:
            raise RuntimeError(f"Failed to read email: {e}")

    def send_email(
        self,
        to: str,
        subject: str,
        body: str
    ) -> Dict:
        """
        Send an email using Gmail API.
        """

        try:

            message = EmailMessage()

            message["To"] = to
            message["Subject"] = subject

            message.set_content(body)

            encoded_message = base64.urlsafe_b64encode(
                message.as_bytes()
            ).decode()

            sent_message = (
                self.service.users()
                .messages()
                .send(
                    userId="me",
                    body={
                        "raw": encoded_message
                    }
                )
                .execute()
            )

            return {
                "status": "success",
                "message_id": sent_message["id"],
                "to": to,
                "subject": subject
}

        except Exception as e:
            raise RuntimeError(
                f"Failed to send email: {e}"
            )

    def _extract_body(self, payload: Dict) -> str:
        """
        Recursively extract the email body from Gmail payload.
        """

        try:
            body = self._find_text_part(payload)

            if not body:
                return ""

            text = base64.urlsafe_b64decode(
                body.encode("UTF-8")
            ).decode("utf-8", errors="ignore")

            # If HTML, convert it to readable text
            if "<html" in text.lower() or "<body" in text.lower():
                soup = BeautifulSoup(text, "html.parser")
                text = soup.get_text(separator="\n")

            # Remove empty lines
            lines = [line.strip() for line in text.splitlines()]
            lines = [line for line in lines if line]

            return "\n".join(lines)

        except Exception:
            return ""
        

        
    def _find_text_part(self, payload: Dict) -> str | None:
        """
        Recursively search for text/plain or text/html content.
        """

        mime_type = payload.get("mimeType", "")

        # Prefer plain text
        if mime_type == "text/plain":
            return payload.get("body", {}).get("data")

        # Fallback to HTML
        if mime_type == "text/html":
            return payload.get("body", {}).get("data")

        # Search nested parts
        for part in payload.get("parts", []):
            result = self._find_text_part(part)
            if result:
                return result

        return None