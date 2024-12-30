import dataclasses


@dataclasses.dataclass(frozen=True)
class RecognizedData:
    text: str = ""
    err: str | None = None