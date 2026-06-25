from gmail_service import GmailService

gmail_service = GmailService()

emails = gmail_service.get_recent_emails(limit=3)

latest_email = emails[0]

email = gmail_service.read_email(latest_email["id"])

print("=" * 80)
print("FROM    :", email["from"])
print("SUBJECT :", email["subject"])
print("DATE    :", email["date"])
print("=" * 80)
print(email["body"])