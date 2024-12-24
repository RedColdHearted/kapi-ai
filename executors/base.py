import os
from abc import ABC

AppPaths = dict[str, str]

NOT_IMPLEMENTED_MASSAGE = (
    "Functionality not implemented in abstract class"
)

class AbstractAppExecuter(ABC):
    """Abstract class that contains operations to execute apps for each os."""

    app_name: str

    def anywhere(self) -> bool:
        raise NotImplementedError(NOT_IMPLEMENTED_MASSAGE)

    def on_windows(self) -> bool:
        raise NotImplementedError(NOT_IMPLEMENTED_MASSAGE)

    def on_linux(self) -> bool:
        raise NotImplementedError(NOT_IMPLEMENTED_MASSAGE)


class CallableExecute(AbstractAppExecuter):

    def call(self, os_name: str, *args, **kwargs):
        if "anywhere" in dir(self):
            return self.anywhere(*args, **kwargs)

        method = self.__getattribute__(f"on_{os_name.lower()}")
        return method(*args, **kwargs)


class PathableExecute(AbstractAppExecuter):

    paths: AppPaths

    def on_windows(self):
        return os.system(self.paths["windows"])

    def on_linux(self):
        return os.system(self.paths["linux"])
