import argparse
from auth import get_gmail_service
from functions.get_recent_mail import get_recent_mail

def main():
    parser = argparse.ArgumentParser(description="Term-Mail: Your Terminal Email Client")
    parser.add_argument("--login", action="store_true", help="Connect to Google and test authentication")
    parser.add_argument("--recent", type=int, metavar="N", help="Read the N of most recent emails")
    args = parser.parse_args()

    if args.login:
        print("Connecting to Google...")
        
        service = get_gmail_service()
        if service:
            print("Success...You are fully authenticated!.")
            
    elif args.recent:
        get_recent_mail(limit=args.recent)
        
    else:
        parser.print_help()
        
if __name__ == "__main__":
    main()
