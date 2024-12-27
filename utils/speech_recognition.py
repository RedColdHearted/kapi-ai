import dataclasses


@dataclasses.dataclass(frozen=True)
class RecognizedAudioData:
    text: str | None
    err: str | None