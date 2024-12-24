import webbrowser

from .base import CallableExecute, PathableExecute
from .exceptions import InvalidBrowserUrl


DEFAULT_BROWSER_URL = "https://google.com"


class Browser(CallableExecute):

    app_name = "browser"

    def __init__(self, url: str = DEFAULT_BROWSER_URL):
        if not url.startswith("https://"):
            raise InvalidBrowserUrl()
        self.url = url

    def anywhere(self) -> bool:
        return webbrowser.open_new_tab(self.url)


class Calculator(PathableExecute, CallableExecute):

    app_name = "calculator"
    paths = {
        "windows": "C:\Windows\System32\calc.exe",
    }


class FileExplorer(PathableExecute, CallableExecute):

    app_name = "file_explorer"
    paths = {
        "windows": "C:\Windows\explorer.exe",
    }


class Telegram(PathableExecute):
    # TODO: Implementation
    pass
