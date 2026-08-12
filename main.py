import argparse
from auth import get_gmail_service
from functions.get_recent_mail import get_recent_mail
from functions.read_mail_by_id import read_mail_by_id
from functions.send_mail import send_mail

def main():
    parser = argparse.ArgumentParser(description="Term-Mail: Your Terminal Email Client")
    parser.add_argument("--login", action="store_true", help="Connect to Google and test authentication")
    parser.add_argument("--recent", type=int, metavar="N", help="Read the N of most recent emails")
    parser.add_argument("--read", type=str, metavar="ID", help="Read the full body of a mail by its ID")
    parser.add_argument("--to", type=str, metavar="test@test.com", help="The mail of the receipient")
    parser.add_argument("--subject", type=str, metavar="subject", help="Mail Subject")
    parser.add_argument("--body", type=str, help="Body of the mail")
    parser.add_argument("--send", action="store_true", help="Sends an email")
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

    elif args.send:
        send_mail(args.to, args.subject, args.body)
        print("Success, email sent!")
    else:
        parser.print_help()
        
if __name__ == "__main__":
    main()
