import argparse
from pathlib import Path

import pddl.core
from pddl import parse_domain, parse_problem

from planification_automatique.pddl_problem import PDDLProblem


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
    pddl_problem: PDDLProblem = PDDLProblem(problem)
    state = pddl_problem.initial_state
    state = pddl_problem.apply_action(state, pddl_problem.applicable_actions(state)[1])
    print(len(pddl_problem.applicable_actions(state)))


if __name__ == "__main__":
    main()
