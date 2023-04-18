from typing import TYPE_CHECKING

from planification_automatique.search_algorithm import SearchAlgorithm

if TYPE_CHECKING:
    from planification_automatique.pddl_problem import PDDLProblem


class AStar(SearchAlgorithm):
    def __init__(self, heuristic):
        super().__init__(heuristic)

    def search(self, problem: PDDLProblem):
        raise NotImplementedError
