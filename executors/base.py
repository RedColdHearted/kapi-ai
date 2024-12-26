import platform
import subprocess
from abc import ABC

AppPaths = dict[str, str]

NOT_IMPLEMENTED_MASSAGE = (
    "Functionality not implemented in abstract class"
)

class BaseExecute(ABC):
    """Base class of methods to execute apps for each os."""

    name: str
    """Name of the app to execute."""
    metadata: dict[str, str] = {}
    """Storage of app execution process."""
    _os_name = platform.system().lower()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def anywhere(self) -> bool:
        """Run app on any os."""
        raise NotImplementedError(NOT_IMPLEMENTED_MASSAGE)

    def on_windows(self) -> bool:
        """Run app on Windows."""
        raise NotImplementedError(NOT_IMPLEMENTED_MASSAGE)

    def on_linux(self) -> bool:
        """Run app on Linux."""
        raise NotImplementedError(NOT_IMPLEMENTED_MASSAGE)

    def on_darwin(self) -> bool:
        """Run app on Mac."""
        raise NotImplementedError(NOT_IMPLEMENTED_MASSAGE)

    def call(self, *args, **kwargs):
        try:
            method = self.__getattribute__(f"on_{self._os_name}")
            return method(*args, **kwargs)
        except NotImplementedError:
            return self.anywhere(*args, **kwargs)

    def to_dict(self):
        return {
            "name": self.name,
            "metadata": self.metadata,
        }


class PathableExecute(BaseExecute):

    paths: AppPaths

    def anywhere(self) -> None:
        try:
            process = subprocess.Popen([self.paths[self._os_name]])
            self.metadata["is_running"] = True
            self.metadata["process_pid"] = process.pid
            return
        except FileNotFoundError:
            self.metadata["is_running"] = False
            self.metadata["err"] = "File not found"

    def to_dict(self):
        dictionary = super().to_dict()
        dictionary["paths"] = self.paths
        return dictionary
