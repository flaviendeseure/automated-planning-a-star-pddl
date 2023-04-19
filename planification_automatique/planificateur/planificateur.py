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
    
    def verify_solution(self, plan: list) -> bool:
        state = self.problem.initial_state
        for action in plan:
            state = self.problem.apply_action(state, action)
        return self.problem.is_goal(state)
