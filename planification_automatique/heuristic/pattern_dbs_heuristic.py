from itertools import product
from typing import AbstractSet

import pddl.logic.base as logic
from pddl.logic import Predicate

from planification_automatique.heuristic import Heuristic
from planification_automatique.pddl_problem import PDDLProblem


class PatternDBsHeuristic(Heuristic):
    def __init__(self, problem: PDDLProblem) -> None:
        super().__init__()
        self.problem = problem
        self.domain = problem.domain
        self.pattern_dbs = self._ground_predicates()

    def _ground_predicates(self) -> dict:
        grounded_predicates: dict = {}
        for predicate in self.domain.predicates:
            actions_list: list = []
            if not predicate.terms:
                grounded_predicates[predicate.name] = [{
                    "name": predicate.name,
                    "terms": [],
                    "objects": []
                }]
                continue

            grounded_action: dict = {
                "name": predicate.name,
                "terms": predicate.terms,
                "objects": []
            }
            possible_objects: list = [
                [
                    obj
                    for obj in self.problem.problem.objects
                    if obj.type_tags == term.type_tags or len(obj.type_tags) == 0
                ]
                for term in predicate.terms
            ]

            for objects in product(*possible_objects):
                grounded_action["objects"] = objects
                actions_list.append(grounded_action.copy())
            grounded_predicates[predicate.name] = actions_list

        return grounded_predicates

    def __call__(self, state: AbstractSet[logic.Formula], goal: logic.Formula) -> int:
        # This function should calculate the heuristic value for the given state and goal,
        # using the pattern databases stored in self.pattern_dbs.

        # Initialize the heuristic value to zero
        h = 0

        # Iterate over all predicates in the goal formula
        if isinstance(goal, Predicate):
            if all(goal.name != p.name for p in state):
                return len(self.pattern_dbs[goal.name])
            return h

        elif isinstance(goal, logic.And):
            for predicate in goal.operands:
                if all(predicate.name != p.name for p in state):
                    h += len(self.pattern_dbs[predicate.name])

        return h
