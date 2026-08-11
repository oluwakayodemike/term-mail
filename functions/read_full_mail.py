from googleapiclient.errors import HttpError
import base64
import sys
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent

if str(parent_dir) not in sys.path:
    sys.path.append(str(parent_dir))

from auth import get_gmail_service

def read_full_mail():
    try:
        service = get_gmail_service()
        msg_data = service.users().messages().get(
            userId="me", 
            id="19febca7b230a6bb",
            format="full",
            metadataHeaders=["Subject"]
        ).execute()

        headers = msg_data["payload"]["headers"]
        parts = msg_data["payload"].get("parts", [])
        
        subject = "Absolutely Nothing"
        msg_body = None

        # checks if msg body is sitting directly in main payloaod
        if "data" in msg_data["payload"]["body"]:
            msg_body = msg_data["payload"]["body"]["data"]

        # or buried in part list?
        else:
            for part in parts:
                if part["mimeType"] == "text/plain":
                    msg_body = part["body"]["data"]
                    break 

        for header in headers:
            if header["name"].lower() == "subject":
                subject = header["value"]
                break
                
        if not msg_body:
            print(f"- {subject}\n   [No plain text body found in this email]")
            return
            
        # kept getting `binascii.Error: Incorrect padding`
        # because google is stripping off some == in an attempt to save a few bytes of internet traffic
        missing_padding = len(msg_body) % 4
        if missing_padding:
            msg_body += "=" * (4 - missing_padding)
            
        cleaned_body = base64.urlsafe_b64decode(msg_body).decode("utf-8", errors="ignore")
        
        print(f"- {subject}")
        print(f"    {cleaned_body}")
    except HttpError as error:
        raise Exception(f"An error occured: {error}")

if __name__ == "__main__":
    read_full_mail()