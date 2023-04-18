from typing import AbstractSet

import pddl.logic.base as logic

from planification_automatique.heuristic import Heuristic


class OneHeuristic(Heuristic):
    def __init__(self):
        super().__init__()

    def __call__(self, state: AbstractSet[logic.Formula], goal: logic.Formula):
        return 1
