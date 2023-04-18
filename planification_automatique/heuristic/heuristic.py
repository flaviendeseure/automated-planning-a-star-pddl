from abc import ABC, abstractmethod
from typing import AbstractSet

import pddl.logic.base as logic


class Heuristic(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def __call__(self, state: AbstractSet[logic.Formula], goal: logic.Formula):
        raise NotImplementedError
