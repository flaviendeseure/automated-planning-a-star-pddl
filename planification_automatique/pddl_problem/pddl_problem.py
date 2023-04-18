from itertools import product
from typing import AbstractSet

import pddl
import pddl.core
import pddl.core
import pddl.logic.base as logic

from planification_automatique.utils import is_applicable, change_state


class PDDLProblem:
    def __init__(self, problem: pddl.core.Problem) -> None:
        self.problem: pddl.core.Problem = problem

    @property
    def initial_state(self) -> AbstractSet[logic.Formula]:
        return self.problem.init

    @property
    def goal(self) -> logic.Formula:
        return self.problem.goal

    @property
    def domain(self) -> pddl.core.Domain:
        return self.problem.domain

    def is_goal(self, state: AbstractSet[logic.Formula]):
        if len(state) != len(self.goal.operands):
            return False

        for operand in self.goal.operands:
            if operand not in state:
                return False
        return True

    def ground_actions(self) -> list[dict]:
        grounded_actions: list = []
        for action in self.domain.actions:
            if not action.parameters:
                grounded_actions.append({
                    "name": action.name,
                    "parameters": [],
                    "precondition": action.precondition,
                    "effect": action.effect,
                    "objects": []
                })
                continue

            grounded_action: dict = {
                "name": action.name,
                "parameters": action.parameters,
                "precondition": action.precondition,
                "effect": action.effect,
                "objects": []
            }
            possible_objects: list = [
                [
                    obj
                    for obj in self.problem.objects
                    if obj.type_tags == parameter.type_tags or len(obj.type_tags) == 0
                ]
                for parameter in action.parameters
            ]

            for objects in product(*possible_objects):
                grounded_action["objects"] = objects
                grounded_actions.append(grounded_action.copy())

        return grounded_actions

    def applicable_actions(self, state: AbstractSet[logic.Formula]) -> list[dict]:
        return [
            action
            for action in self.ground_actions()
            if is_applicable(action, state)
        ]

    @staticmethod
    def apply_action(
            state: AbstractSet[logic.Formula], action: dict
    ) -> set[logic.Formula]:
        return change_state(state, action)
