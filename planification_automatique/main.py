import argparse
from pathlib import Path

from pddl import parse_domain, parse_problem
import pddl.logic.base as logic


def is_applicable(action, state):
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--group", type=int, default=1)
    parser.add_argument("--problem", type=str, default="problem1.pddl")
    parser.add_argument("--domain", type=str, default="domain.pddl")

    # Parse args
    args = parser.parse_args()

    folder = Path("planification_automatique/data")
    group = folder / f"groupe{args.group}"
    domain = parse_domain(group / args.domain)
    problem = parse_problem(group / args.problem)
    problem.domain = domain
    # print(problem.init)
    # print(problem.domain)
    # print(problem.requirements)
    # print(problem.objects)
    # print(problem.goal)
    # print(problem.domain.actions)
    for action in problem.domain.actions:
        # print(action.precondition)
        # print(action.effect)
        # print(action.parameters)
        # print(action.name)
        # is_applicable(action, problem.init)
        break


if __name__ == "__main__":
    main()
