from googleapiclient.errors import HttpError
import sys
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent

if str(parent_dir) not in sys.path:
    sys.path.append(str(parent_dir))

from auth import get_gmail_service

def thrash_mail_by_id(message_id: str):
    try:
        service = get_gmail_service()

        service.users().messages().trash(
            userId="me",
            id=message_id
        ).execute()

    except HttpError as error:
        raise Exception(f"An error occured while deleting mail: {error}")