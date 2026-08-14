import argparse
import tempfile, subprocess, os
from auth import get_gmail_service
from functions.get_recent_mail import get_recent_mail
from functions.read_mail_by_id import read_mail_by_id
from functions.send_mail import send_mail
from functions.archive_mail import archive_mail
from functions.trash_mail import trash_mail_by_id

def main():
    parser = argparse.ArgumentParser(description="Term-Mail: Your Terminal Email Client")
    parser.add_argument("--login", action="store_true", help="Connect to Google and test authentication")
    parser.add_argument("--recent", type=int, metavar="N", help="Read the N of most recent emails")
    parser.add_argument("--search", type=str, metavar="is:unread", help="Search gmail using gmail syntax... i.e is:unread")
    parser.add_argument("--read", type=str, metavar="ID", help="Read the full body of a mail by its ID")
    parser.add_argument("--to", type=str, metavar="test@test.com", help="The mail of the receipient")
    parser.add_argument("--subject", type=str, metavar="subject", help="Mail Subject")
    parser.add_argument("--body", type=str, help="Body of the mail")
    parser.add_argument("--send", action="store_true", help="Sends an email")
    parser.add_argument("--archive", type=str, metavar="ID", help="Archives a mail using the ID")
    parser.add_argument("--trash", type=str, metavar="ID", help="Deletes a mail using the ID")
    args = parser.parse_args()

    if args.login:
        print("Connecting to Google...")
        
        service = get_gmail_service()
        if service:
            print("Success...You are fully authenticated!.")
            
    elif args.recent:
        emails = get_recent_mail(limit=args.recent)

        for email in emails:
            print(f"-[{email["id"]}]: {email["subject"]}")
            print(f"    {email["snippet"]}")
        
    elif args.read:
        read_mail_by_id(message_id=args.read)
        
    elif args.search:
        limit = args.recent if args.recent else 10
        get_recent_mail(limit=limit, query=args.search)

    elif args.archive:
        archive_mail(message_id=args.archive)

    elif args.trash:
        trash_mail_by_id(message_id=args.trash)
        
    elif args.send:
        if args.send and not args.to and not args.subject and not args.body:
            # this creates a temporary .txt file and allow users to modify it
            # then captures the input
            tf = tempfile.NamedTemporaryFile(mode="w+",suffix=".txt", delete=False) # delete=False stops file from instantly deleting on tf.close() 
            try:
                # template for user to follow
                template = (
                    "To: \n"
                    "Subject: \n"
                    "\n"
                    "# ---email body goes below this line---\n"
                )
                tf.write(template)
                tf.close()
                
                subprocess.run(["vi", tf.name], check=True)

                to_addr, subject, bodies = None, None, []
                
                with open(tf.name, 'r') as f:
                    for line in f:
                        if line.startswith("To:"):
                            to_addr = line.replace("To:", "").strip()
                        elif line.startswith("Subject:"):
                            subject = line.replace("Subject:", "").strip()
                        elif not line.startswith("#"): # ignore comment
                            bodies.append(line)

                body_text = "".join(bodies).strip()

                if not to_addr or not subject or not body_text:
                    print("Error: email not sent. some fields were blank")
                    return
                    

                print(body_text)
                print(f"sending email to {to_addr}...")
                send_mail(to_addr, subject, body_text)

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
