import argparse
import time
from pathlib import Path
from typing import AbstractSet

import pddl.core
import pddl.logic.base as logic
from pddl import parse_domain, parse_problem

from planification_automatique.heuristic import OneHeuristic, ManhattanDistanceHeuristic
from planification_automatique.pddl_problem import PDDLProblem
from planification_automatique.planificateur import Planificateur
from planification_automatique.search_algorithm.a_star import AStar


def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("--group", type=int, default=1)
    parser.add_argument("--problem", type=str, default="problem0")
    parser.add_argument("--domain", type=str, default="domain")

    args: argparse.Namespace = parser.parse_args()

    data_folder: Path = Path("planification_automatique/data")
    group: str = f"groupe{args.group}"
    problem_file: Path = (data_folder / group / args.problem).with_suffix(".pddl")
    domain_file: Path = (data_folder / group / args.domain).with_suffix(".pddl")
    problem: pddl.core.Problem = parse_problem(problem_file)
    problem.domain = parse_domain(domain_file)
    pddl_problem: PDDLProblem = PDDLProblem(problem)

    one_heuristic: OneHeuristic = OneHeuristic()
    a_star: AStar = AStar(one_heuristic)
    planificateur: Planificateur = Planificateur(pddl_problem, a_star)

    start: float = time.perf_counter()
    solution, cost, plan = planificateur.solve()
    end: float = time.perf_counter()

    print("=========================================================")
    print(f"Domain: groupe{args.group} - {args.domain}")
    print(f"Problem: {args.problem}")
    print("=========================================================")
    if not solution:
        print("No solution found")
        return

    is_valid_plan: bool = planificateur.verify_solution(plan)
    if not is_valid_plan:
        print("Plan is not correct")
        return

    state: AbstractSet[logic.Formula] = pddl_problem.initial_state
    for action in plan:
        state = pddl_problem.apply_action(state, action)
    print(
        "Solution found with cost {cost} in {plan_size} steps and {time:.2f} seconds"
        .format(cost=cost, plan_size=len(plan), time=end - start)
    )
    print("-----------------------------------------")
    print("Found Plan:")
    print("-----------")
    text_plans = " => ".join([f"{action['name']}({', '.join([str(obj) for obj in action['objects']])})" for action in plan])
    print(text_plans)
    print("=========================================================")


if __name__ == "__main__":
    main()
