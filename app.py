from textual.app import App, ComposeResult
from textual.containers import HorizontalScroll, VerticalScroll
from textual.screen import Screen
from textual.widgets import Placeholder, Header, Footer

class ColumnsContainer(Placeholder):
    DEFAULT_CSS = """
    ColumnsContainer {
        width: 1fr;
        height: 1fr;
        border: solid white;
    }
    """

class EmailItem(Placeholder):
    DEFAULT_CSS = """
    EmailItem {
        height: 5;
        width: 1fr;
        border: tall $background;
    }
    """

class LeftColumn(VerticalScroll):
    DEFAULT_CSS = """
    LeftColumn {
        height: 1fr;
        width: 35;
        margin: 0 2;
        border-right: solid white;
    }
    """
    def compose(self) -> ComposeResult:
        for mail_no in range(1, 20):
            yield EmailItem(id=f"Mail{mail_no}")

class RightColumn(VerticalScroll):
    DEFAULT_CSS = """
    RightColumn {
        height: 1fr;
        width: 1fr;
        margin: 0 2;
    }
    """
    def compose(self) -> ComposeResult:
        yield Placeholder("This is where the email body goes ")

class MailScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header(id="Header")  
        # yield ColumnsContainer(id="ColumnsContainer")
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