import argparse
from auth import get_gmail_service

def main():
    parser = argparse.ArgumentParser(description="Term-Mail: Your Terminal Email Client")
    parser.add_argument("--login", action="store_true", help="Connect to Google and test authentication")
    args = parser.parse_args()

    if args.login:
        print("Connecting to Google...")
        
        service = get_gmail_service()
        if service:
            print("Success...You are fully authenticated!.")
    else:
        parser.print_help()
        
if __name__ == "__main__":
    main()
