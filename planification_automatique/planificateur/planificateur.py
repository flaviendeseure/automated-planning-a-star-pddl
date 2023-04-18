from typing import AbstractSet

import pddl.logic.base as logic

from planification_automatique.pddl_problem import PDDLProblem
from planification_automatique.search_algorithm import SearchAlgorithm


class Planificateur:
    def __init__(
            self, problem: PDDLProblem, search_algorithm: SearchAlgorithm,
    ) -> None:
        self.problem = problem
        self.search_algorithm = search_algorithm

    def solve(self) -> (AbstractSet[logic.Formula], int):
        return self.search_algorithm.search(self.problem)
