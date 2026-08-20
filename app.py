from ctypes.util import test
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, ListView, ListItem
from textual import on
from functions.get_recent_mail import get_recent_mail

class EmailItem(ListItem):
    DEFAULT_CSS = """
        EmailItem {
            height: 3;
            width: 1fr;
            color: #cdd6f4;
            background: #1e1e2e;
            layout: horizontal;
            padding: 0 1;
            border-bottom: solid #313244;
        }
        
        .sender {
            width: 35;
        }
        
        .subject {
            width: 1fr;
            overflow: hidden;
        }

        .date {
            width: 10;
            content-align: left middle;
        }
    """
    def __init__(self, email_data: dict, id: str) -> None:
        super().__init__(id=id)
        self.email_data = email_data
    def compose(self) -> ComposeResult:
        yield Static(self.email_data["sender_name"], classes="sender")
        
        display_text = f"{self.email_data['subject']} - {self.email_data['snippet'][:45]}"
        yield Static(display_text, classes="subject")
        yield Static(self.email_data["msg_date"], classes="date")

class MainMenu(ListView):
    DEFAULT_CSS = """
        MainMenu {
            width: 30;
            height: 1fr;
            border: solid #89b4fa;
            background: #1e1e2e;
        }
        
        ListItem {
            padding: 0 2;
        }
        
        ListItem:hover {
            background: #313244;
        }
    """
    def on_mount(self) -> None:
        self.border_title = "Categories"

    def compose(self) -> ComposeResult:
        yield ListItem(Static("Inbox"))
        yield ListItem(Static("Sent"))
        yield ListItem(Static("Drafts"))
        yield ListItem(Static("Trash"))

class MailViewer(Vertical):
    DEFAULT_CSS = """
        MailViewer {
            height: 1.5fr;
            width: 1fr;
            border: solid #a6e3a1;
            background: #1e1e2e;
            padding: 1 2;
        }
    """
    def on_mount(self) -> None:
        self.border_title = "Email Body"

    def compose(self) -> ComposeResult:
        yield Static("Selected Emails will appear here...", id="body-text")
        
class InboxPane(ListView):
    DEFAULT_CSS = """
        InboxPane {
            height: 1fr; 
            width: 1fr;
            border: solid #f9e2af;
            background: #1e1e2e;
            overflow-y: scroll;
        }
    """
    def on_mount(self) -> None:
        self.border_title = "Category Results"

    def compose(self) -> ComposeResult:
        emails = get_recent_mail(limit=15)
        for mail in emails:
            yield EmailItem(email_data=mail, id=f"Mail_{mail['id']}")

class RightWorkspace(Vertical):
    DEFAULT_CSS = """
    RightWorkspace {
        width: 1fr;
        height: 1fr;
    }
    """
    def compose(self) -> ComposeResult:
        yield MailViewer()
        yield InboxPane(id="inbox-list")

class MailScreen(Horizontal):
    DEFAULT_CSS = """
        MailScreen {
            background: #1e1e2e;
        }
    """
    @on(ListView.Selected, "#inbox-list")
    def handle_selected_mail(self, event: ListView.Selected) -> None:
        selected_row = event.item
        email_info = selected_row.email_data

        msg = f"from: {email_info['sender_name']}\nsubject: {email_info['subject']}"

        self.query_one("#body-text", Static).update(msg)
        
    def compose(self) -> ComposeResult:
        yield MainMenu()
        yield RightWorkspace()

class LayoutApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield MailScreen()
        yield Footer()

if __name__ == "__main__":
    app = LayoutApp()
    app.run()