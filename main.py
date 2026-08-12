import argparse
import tempfile, subprocess, os
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
        if args.send and not args.to and not args.subject and not args.body:
            # this creates a temporary .txt file and allow users to modify it
            # then captures the input
            tf = tempfile.NamedTemporaryFile(suffix=".txt", delete=False) # delete=False stops file from instantly deleting on tf.close() 
            try:
                tf.close()
                subprocess.run(["vi", tf.name], check=True)
                with open(tf.name, 'r') as f:
                    text = f.read()

                print("email:", text)
            finally:
                # clean up temporary file
                if os.path.exists(tf.name):
                    os.remove(tf.name)

        elif not args.to or not args.subject or not args.body:
            print("Error: --send requires either ALL flags (--to, --subject, and --body flags) or no flags at all to open an editor.")
            return

        else:
            print(f"sending email to {args.to}...")
            send_mail(args.to, args.subject, args.body)
            print("Success, email sent!")
    else:
        parser.print_help()
        
if __name__ == "__main__":
    main()
