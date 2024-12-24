import platform

from .locals import (
    Browser,
    Calculator,
    FileExplorer,
)

AppParams = dict[str, str | int]

OS_NAME = platform.system()

class ExecutorManager:

    executors = (
        Browser,
        Calculator,
        FileExplorer,
    )

    def run(self, app_name: str, params: AppParams = {}):
        app_name = app_name.lower()
        for executor in self.executors:
            if executor.app_name == app_name:
                if params:
                    instance = executor(**params)
                else:
                    instance = executor()
                instance.call(OS_NAME)
                return True
        return False