import platform

from .locals import (
    Browser,
    Calculator,
    FileExplorer,
)

AppParams = dict[str, str | int]


class ExecutorManager:

    executors = (
        Browser,
        Calculator,
        FileExplorer,
    )

    def run(self, app_name: str, params: AppParams = {}):
        app_name = app_name.lower()
        for Executor in self.executors:
            if Executor.name == app_name:
                app = Executor(**params)
                app.call()
                print(app.to_dict())
                return app.to_dict()
