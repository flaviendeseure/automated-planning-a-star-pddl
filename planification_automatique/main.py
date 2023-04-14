import argparse
from pathlib import Path

import pddl.logic.base as logic
from pddl import parse_domain, parse_problem


def is_applicable(action, state):
    # print(action.precondition.parts)
    print(type(action.precondition))
    print(state)
    if isinstance(action.precondition, logic.Not):
        if isinstance(action.precondition.argument, logic.FalseFormula):
            return True
    elif isinstance(action.precondition, logic.And):
        for operand in action.precondition.operands:
            print(operand)
            print(operand in state)
        return True

    return False


def ground_actions(domain, objects: frozenset):
    grounded_actions: list = []
    for action in domain.actions:
        if not action.parameters:
            grounded_actions.append(action)
        for parameter in action.parameters:
            for obj in objects:
                if obj.type_tags == parameter.type_tags or len(obj.type_tags) == 0:
                    grounded_actions.append(action)
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
    print(f"{len(ground_actions(domain, problem.objects)) = }")
    # print(problem.init)
    # print(problem.domain)
    # print(problem.requirements)
    # print(problem.objects)
    # print(problem.goal)
    # print(problem.domain.actions)
    for action in problem.domain.actions:
        # print(action.precondition)
        # print(action.effect)
        # print(f"{action.parameters = }")
        # print(action.name)

        # is_applicable(action, problem.init)
        break


if __name__ == "__main__":
    main()
