from textual.app import App, ComposeResult
from textual.containers import HorizontalScroll, VerticalScroll
from textual.screen import Screen
from textual.widgets import Header, Footer, Static

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

class LeftColumn(VerticalScroll):
    DEFAULT_CSS = """
    LeftColumn {
        height: 1fr;
        width: 35;
        border-right: solid #89b4fa;
        background: #1e1e2e;
    }
    """
    def compose(self) -> ComposeResult:
        for mail_no in range(1, 20):
            fake_text = f"{mail_no}: Mike Test\nSnip:What are you?"
            yield EmailItem(text=fake_text, id=f"Mail{mail_no}")
            
class RightColumn(VerticalScroll):
    DEFAULT_CSS = """
    RightColumn {
        height: 1fr;
        width: 1fr;
        padding: 1 2;
        background: #1e1e2e;
        color: #cdd6f4;
    }
    """
    def compose(self) -> ComposeResult:
        # Dummy body text
        dummy_body = "18.09.2023 21:19\n\nHello Mike,\n\nThis is where the email content will eventually render after wiring"
        yield Static(dummy_body)

class MailScreen(Screen):
    DEFAULT_CSS = """
    MailScreen {
        background: #1e1e2e;
    }
    """
    def compose(self) -> ComposeResult:
        yield Header(id="Header")  
        with HorizontalScroll():
            yield LeftColumn()
            yield RightColumn()
        yield Footer(id="Footer")

class LayoutApp(App):
    def on_mount(self) -> None:
        self.push_screen(MailScreen())


if __name__ == "__main__":
    app = LayoutApp()
    app.run()