import argparse
from auth import get_gmail_service
from functions.get_recent_mail import get_recent_mail
from functions.read_mail_by_id import read_mail_by_id

def main():
    parser = argparse.ArgumentParser(description="Term-Mail: Your Terminal Email Client")
    parser.add_argument("--login", action="store_true", help="Connect to Google and test authentication")
    parser.add_argument("--recent", type=int, metavar="N", help="Read the N of most recent emails")
    parser.add_argument("--read", type=str, metavar="ID", help="Read the full body of a mail by its ID")
    args = parser.parse_args()

    if args.login:
        print("Connecting to Google...")
        
        service = get_gmail_service()
        if service:
            print("Success...You are fully authenticated!.")
            
    elif args.recent:
        get_recent_mail(limit=args.recent)

    elif args.read:
        read_mail_by_id(message_id=args.read)
        
    else:
        parser.print_help()
        
if __name__ == "__main__":
    main()
