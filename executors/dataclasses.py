from dataclasses import dataclass


@dataclass(frozen=True)
class ExecData:
    status: bool