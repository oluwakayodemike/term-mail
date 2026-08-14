from unittest.mock import DEFAULT
from textual.app import App, ComposeResult
from textual.containers import HorizontalScroll, VerticalScroll
from textual.screen import Screen
from textual.widgets import Header, Footer, Static
from functions.get_recent_mail import get_recent_mail

class EmailItem(Static):
    def __init__(self, text: str, id: str) -> None:
        super().__init__(text, id=id)

    DEFAULT_CSS = """
        EmailItem {
            height: 3;
            width: 1fr;
            color: #cdd6f4;
            background: #1e1e2e;
            padding: 0 1;
            border-bottom: solid #313244;
        }
        """
class MainMenu(VerticalScroll):
    DEFAULT_CSS = """
    MainMenu {
        height: 1fr;
        width: 35;
        background: #1e1e2e;
    }
    """
    pass

class SenderColumn(VerticalScroll):
    DEFAULT_CSS = """
    SenderColumn {
        height: 1fr;
        width: 35;
        background: #1e1e2e;
    }
    """
    def compose(self) -> ComposeResult:
        emails = get_recent_mail(limit=15)

        for mail in emails:
            display_text = f"{mail["sender_name"]}"
            yield EmailItem(text=display_text, id=f"Mail{mail["id"]}")
            
class LeftColumn(VerticalScroll):
    DEFAULT_CSS = """
    LeftColumn {
        height: 1fr;
        width: 1fr;
        border-right: solid #89b4fa;
        background: #1e1e2e;
    }
    """
    def compose(self) -> ComposeResult:
        emails = get_recent_mail(limit=15)

        for mail in emails:
            display_text = f"{mail["subject"]} - {mail["snippet"]}"
            yield EmailItem(text=display_text, id=f"Mail{mail["id"]}")
            
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
            yield SenderColumn()
            yield LeftColumn()
            # yield RightColumn()
        yield Footer(id="Footer")

class LayoutApp(App):
    def on_mount(self) -> None:
        self.push_screen(MailScreen())


if __name__ == "__main__":
    app = LayoutApp()
    app.run()