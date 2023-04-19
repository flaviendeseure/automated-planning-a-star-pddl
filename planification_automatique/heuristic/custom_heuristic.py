from typing import AbstractSet

import pddl.logic.base as logic
from pddl.logic import Predicate

from planification_automatique.heuristic import Heuristic
from planification_automatique.pddl_problem import PDDLProblem


class CustomHeuristic(Heuristic):
    def __init__(self, problem: PDDLProblem) -> None:
        super().__init__()
        self.problem = problem

    def __call__(self, state: AbstractSet[logic.Formula], goal: logic.Formula) -> float:
        if isinstance(goal, Predicate):
            if goal.name != "at":
                goal = logic.And(*[goal, logic.TrueFormula])
                return self.__call__(state, goal)

            position: Predicate | None = next(
                (p for p in state if p.name == goal.name),
                None
            )
            position_state: str = position.terms[0].name
            position_states: tuple = (
                int(position_state[3:-1]), int(position_state[-1])
            )

            position_goal: str = goal.terms[0].name
            position_goals: tuple = (int(position_goal[3:-1]), int(position_goal[-1]))

            return abs(position_states[0] - position_goals[0]) + abs(
                position_states[1] - position_goals[1]
            )

        if isinstance(goal, logic.And):
            h: int = 0
            for subgoal in goal.operands:
                if isinstance(subgoal, logic.TrueFormula):
                    continue

                if subgoal in state:
                    continue

                h += 1

            return h

        else:
            raise NotImplementedError
