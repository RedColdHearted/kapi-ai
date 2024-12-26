import webbrowser

from .base import BaseExecute, PathableExecute
from .exceptions import InvalidBrowserUrl


DEFAULT_BROWSER_URL = "https://google.com"


class Browser(BaseExecute):

    name = "browser"

    def __init__(self, url: str = DEFAULT_BROWSER_URL, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not url.startswith("https://"):
            raise InvalidBrowserUrl()
        self.url = url

    def anywhere(self) -> bool:
        webbrowser.open_new_tab(self.url)
        self.metadata["is_running"] = True


class Calculator(PathableExecute):

    name = "calculator"
    paths = {
        "windows": "C:\\Windows\\System32\\calc.exe",
    }


class FileExplorer(PathableExecute):

    name = "file_explorer"
    paths = {
        "windows": "C:\\Windows\\explorer.exe",
    }


class Telegram(PathableExecute):
    # TODO: Implementation
    pass
