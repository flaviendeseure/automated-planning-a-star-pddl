import argparse
from itertools import product
from pathlib import Path
from typing import AbstractSet

import pddl.core
import pddl.logic.base as logic
from pddl import parse_domain, parse_problem
from pddl.logic.predicates import Predicate


def construct_predicate(predicate: Predicate, action: dict) -> Predicate:
    variables = []
    for term, parameter, obj in zip(
            predicate.terms, action["parameters"], action["objects"]
    ):
        if term == parameter:
            variables.append(obj)
    return Predicate(predicate.name, *variables)


def is_applicable(action: dict, state: frozenset) -> bool:
    preconditions = action["precondition"]
    if isinstance(preconditions, logic.TrueFormula):
        return True

    elif isinstance(preconditions, logic.FalseFormula):
        return False

    elif isinstance(preconditions, logic.Not):
        new_action = action.copy()
        new_action["precondition"] = preconditions.argument
        return not is_applicable(new_action, state)

    elif isinstance(preconditions, logic.And):
        for operand in preconditions.operands:
            new_action = action.copy()
            new_action["precondition"] = operand
            if not is_applicable(new_action, state):
                return False
        return True

    elif isinstance(preconditions, logic.Or):
        for operand in preconditions.operands:
            new_action = action.copy()
            new_action["precondition"] = operand
            if is_applicable(new_action, state):
                return True
        return False

    elif isinstance(preconditions, Predicate):
        predicate: Predicate = construct_predicate(preconditions, action)
        return predicate in state

    else:
        print(preconditions)
        print(type(preconditions))
        raise NotImplementedError


def ground_actions(problem: pddl.core.Problem) -> list[dict]:
    grounded_actions: list = []
    for action in problem.domain.actions:
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
                for obj in problem.objects
                if obj.type_tags == parameter.type_tags or len(obj.type_tags) == 0
            ]
            for parameter in action.parameters
        ]

        for objects in product(*possible_objects):
            grounded_action["objects"] = objects
            grounded_actions.append(grounded_action.copy())

    return grounded_actions


def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("--group", type=int, default=1)
    parser.add_argument("--problem", type=str, default="problem1")
    parser.add_argument("--domain", type=str, default="domain")

    # Parse args
    args: argparse.Namespace = parser.parse_args()

    data_folder: Path = Path("planification_automatique/data")
    group: str = f"groupe{args.group}"
    problem_file: Path = (data_folder / group / args.problem).with_suffix(".pddl")
    domain_file: Path = (data_folder / group / args.domain).with_suffix(".pddl")
    problem: pddl.core.Problem = parse_problem(problem_file)
    problem.domain = parse_domain(domain_file)

    grounded_actions: list[dict] = ground_actions(problem)
    print(f"{len(grounded_actions)} actions grounded in domain")
    possible_actions: list = [
        action
        for action in grounded_actions
        if is_applicable(action, problem.init)
    ]
    print(f"{len(possible_actions)} actions possible in initial state")


if __name__ == "__main__":
    main()
