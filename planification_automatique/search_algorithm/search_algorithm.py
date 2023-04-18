from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from planification_automatique.heuristic import Heuristic

if TYPE_CHECKING:
    from planification_automatique.pddl_problem import PDDLProblem


class SearchAlgorithm(ABC):
    def __init__(self, heuristic: Heuristic) -> None:
        self.heuristic = heuristic

    @abstractmethod
    def search(self, problem: PDDLProblem):
        raise NotImplementedError
