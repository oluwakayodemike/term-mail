from googleapiclient.errors import HttpError
import base64
import sys
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent

if str(parent_dir) not in sys.path:
    sys.path.append(str(parent_dir))

from auth import get_gmail_service

def extract_email_body(payload: dict, target_mime):
    parts_queue = [payload]

    # while there's still parts to check, continue
    while len(parts_queue) > 0:
        current_part = parts_queue.pop(0)

        # prevents crashes incase google returns wierd data instead of a `dict`  
        if isinstance(current_part, dict):
            # if mime matches the exact mimetype we want (text/plain) and has the actual data
            # return it
            if current_part.get("mimeType") == target_mime and "data" in current_part.get("body", {}):
                return current_part["body"]["data"]

            # if text not found, check for smaller sub-parts in it
            if "parts" in current_part:
                for sub_part in current_part["parts"]:
                    # move smaller parts to the back of the list to check on next loops
                    parts_queue.append(sub_part)

    return None
    
def read_mail_by_id(message_id: str):
    try:
        service = get_gmail_service()
        msg_data = service.users().messages().get(
            userId="me", 
            id=message_id,
            format="full"
        ).execute()

        payload = msg_data.get("payload", {})
        headers = payload.get("headers", [])
        
        subject = "Absolutely Nothing"
        msg_mime = payload.get("mimeType")
        msg_body = None

        for header in headers:
            if header["name"].lower() == "subject":
                subject = header["value"]
                break
                
        # checks if msg body is sitting directly at the top in the payload (plain text/html)
        if msg_mime == "text/plain" and "data" in payload.get("body", {}):
            msg_body = payload["body"]["data"]
        elif msg_mime == "text/html" and "data" in payload.get("body", {}):
            msg_body = payload["body"]["data"]
            
        # else, dig for plain text. if that fails, dig for HTML.
        else:
            msg_body = extract_email_body(payload, "text/plain") or extract_email_body(payload, "text/html")

        if not msg_body:
            print(f"- {subject}\n   [No readable body found in this email]")
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