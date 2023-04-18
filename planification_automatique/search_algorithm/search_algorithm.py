from abc import ABC, abstractmethod

from planification_automatique.heuristic import Heuristic
from planification_automatique.pddl_problem import PDDLProblem


class SearchAlgorithm(ABC):
    def __init__(self, heuristic: Heuristic) -> None:
        self.heuristic = heuristic

    @abstractmethod
    def search(self, problem: PDDLProblem):
        raise NotImplementedError
