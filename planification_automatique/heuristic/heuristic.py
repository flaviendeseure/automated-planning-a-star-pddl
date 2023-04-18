from abc import ABC
from typing import AbstractSet

import pddl.logic.base as logic


class Heuristic(ABC):
    def __init__(self) -> None:
        pass

    def __call__(
            self, state: AbstractSet[logic.Formula], action: dict, goal: logic.Formula
    ):
        raise NotImplementedError
