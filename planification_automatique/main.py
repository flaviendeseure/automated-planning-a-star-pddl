import argparse
from pathlib import Path

import pddl.logic.base as logic
from pddl.logic.predicates import Predicate
from pddl import parse_domain, parse_problem


def is_applicable(action, state):
    # print(action.precondition.parts)
    # print(type(action.precondition))
    print(f"{state = }")
    if isinstance(action.precondition, logic.Not):
        if isinstance(action.precondition.argument, logic.FalseFormula):
            return True
    elif isinstance(action.precondition, logic.And):
        print(action)
        for operand in action.precondition.operands:
            print(operand in state)
            if operand not in state:
                print(operand)
        return True

    elif isinstance(action.precondition, Predicate):
        print(action)
        print(action.precondition)
        print(action.precondition in state)
        raise NotImplementedError(action.precondition)

    else:
        print(action.precondition)
        print(type(action.precondition))
        raise NotImplementedError
    return False


def ground_actions(domain, objects: frozenset):
    grounded_actions: list = []
    for action in domain.actions:
        if not action.parameters:
            grounded_actions.append(action)
        grounded_action: dict = {
            "name": action.name,
            "parameters": action.parameters,
            "precondition": action.precondition,
            "effect": action.effect,
            "objects": []
        }
        for parameter in action.parameters:
            for obj in objects:
                if obj.type_tags == parameter.type_tags or len(obj.type_tags) == 0:
                    grounded_action["objects"].append(obj)
                    break
        if len(grounded_action["objects"]) == len(action.parameters):
            grounded_actions.append(grounded_action)
    return grounded_actions


def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("--group", type=int, default=1)
    parser.add_argument("--problem", type=str, default="problem1.pddl")
    parser.add_argument("--domain", type=str, default="domain.pddl")

    # Parse args
    args: argparse.Namespace = parser.parse_args()

    data_folder = Path("planification_automatique/data")
    group: str = f"groupe{args.group}"
    domain = parse_domain(data_folder / group / args.domain)
    problem = parse_problem(data_folder / group / args.problem)
    problem.domain = domain
    grounded_actions = ground_actions(domain, problem.objects)
    print(len(grounded_actions))
    # for action in grounded_actions:
    #     print(is_applicable(action, problem.init))
    # print(problem.init)
    # print(problem.domain)
    # print(problem.requirements)
    # print(problem.objects)
    # print(problem.goal)
    # print(problem.domain.actions)
    # for action in problem.domain.actions:
        # print(action.precondition)
        # print(action.effect)
        # print(f"{action.parameters = }")
        # print(action.name)

        # is_applicable(action, problem.init)
        # break


if __name__ == "__main__":
    main()
