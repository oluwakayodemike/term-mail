from textual.app import App, ComposeResult
from textual.containers import HorizontalScroll, VerticalScroll, Horizontal
from textual.screen import Screen
from textual.widgets import Header, Footer, Static
from functions.get_recent_mail import get_recent_mail

class EmailItem(Horizontal):
    DEFAULT_CSS = """
        EmailItem {
            height: 3;
            width: 1fr;
            color: #cdd6f4;
            background: #1e1e2e;
            padding: 0 1;
            border-bottom: solid #313244;
        }
        
        .sender {
            width: 35;
        }
        
        .subject {
            width: 1fr;
        }

        .date {
            width: 10;
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
        
class MainMenu(VerticalScroll):
    DEFAULT_CSS = """
        MainMenu {
            height: 1fr;
            width: 35;
            background: #1e1e2e;
        }
    """
    pass

class InboxPane(VerticalScroll):
    DEFAULT_CSS = """
        InboxPane {
            height: 1fr;
            width: 1fr;
            border-right: solid #89b4fa;
            background: #1e1e2e;
        }
    """
    def compose(self) -> ComposeResult:
        emails = get_recent_mail(limit=15)
        for mail in emails:
            yield EmailItem(email_data=mail, id=f"Mail_{mail["id"]}")

# class RightColumn(VerticalScroll):
#     DEFAULT_CSS = """
#     RightColumn {
#         height: 1fr;
#         width: 1fr;
#         padding: 1 2;
#         background: #1e1e2e;
#         color: #cdd6f4;
#     }
#     """
#     def compose(self) -> ComposeResult:
#         # Dummy body text
#         dummy_body = "18.09.2023 21:19\n\nHello Mike,\n\nThis is where the email content will eventually render after wiring"
#         yield Static(dummy_body)

class MailScreen(Screen):
    DEFAULT_CSS = """
        MailScreen {
            background: #1e1e2e;
        }
    """
    def compose(self) -> ComposeResult:
        yield Header(id="Header")  
        with HorizontalScroll():
            yield MainMenu()
            yield InboxPane()
        yield Footer(id="Footer")

class LayoutApp(App):
    def on_mount(self) -> None:
        self.push_screen(MailScreen())


if __name__ == "__main__":
    app = LayoutApp()
    app.run()