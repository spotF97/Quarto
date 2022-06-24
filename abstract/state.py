from __future__ import annotations
from abc import ABC, abstractmethod

class State(ABC):

    @abstractmethod
    def legal_actions(self) -> list:
        pass

    @abstractmethod
    def random_action(self):
        pass

    @abstractmethod
    def next(self, action) -> State:
        pass

    @abstractmethod
    def is_lose(self) -> bool:
        pass

    @abstractmethod
    def is_draw(self) -> bool:
        pass

    @abstractmethod
    def is_done(self) -> bool:
        pass

    @abstractmethod
    def is_first_player(self) -> bool:
        pass