from typing import Dict
from googleapiclient.errors import HttpError
import html
import sys
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent

if str(parent_dir) not in sys.path:
    sys.path.append(str(parent_dir))
    
from auth import get_gmail_service

def get_recent_mail(limit: int = 5, query: str = "in:inbox") -> list[dict[str, str]]:
    recent_mail = []
    try:
        service = get_gmail_service()
        results = service.users().messages().list(userId="me", maxResults=limit, q=query).execute()
        messages = results.get('messages', [])

        if not messages:
            print("inbox is empty!")
        for msg in messages:
            # using format as metadata to grab only headers makes it very fast
            msg_data = service.users().messages().get(
                userId="me",
                id=msg["id"],
                format="metadata",
                metadataHeaders=["Subject"]
            ).execute()

            headers = msg_data["payload"]["headers"]
            
            subject = "Absolutely Nothing"

            for header in headers:
                if header["name"].lower() == 'subject':
                    subject = header["value"]
                    break

            snippet = msg_data.get('snippet', '')
            cleaned_snippet = html.unescape(snippet)

            recent_mail.append({
                "id": msg["id"],
                "subject": subject,
                "snippet": cleaned_snippet
            })
    except HttpError as error:
        raise Exception(f"An error occured: {error}")

    return recent_mail