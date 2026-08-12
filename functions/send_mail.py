from email.message import EmailMessage
from googleapiclient.errors import HttpError
import base64
import sys
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent

if str(parent_dir) not in sys.path:
    sys.path.append(str(parent_dir))

from auth import get_gmail_service

def send_mail(to_address: str, subject: str, body: str):
    try:
        service = get_gmail_service()
        message = EmailMessage()

        message.set_content(body)

        message["To"] = to_address
        message["From"] = "iammichaelkayode@gmail.com"
        message["Subject"] = subject

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        create_message = {"raw": encoded_message}

        send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )

        print(f"Message Id: {send_message["id"]}")
    except HttpError as error:
        raise Exception(f"An error occured: {error}")
    
# if __name__ == "__main__":
#     create_mail()