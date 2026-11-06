from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class Hit:
    text: str
    type: str


class DetectorBase(ABC):
    @abstractmethod
    def detect(self, text: str) -> list[Hit]:
        ...
