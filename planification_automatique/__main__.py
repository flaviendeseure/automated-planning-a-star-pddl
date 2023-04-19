import argparse
import json
import time
from pathlib import Path

import pddl.core
from pddl import parse_domain, parse_problem

from planification_automatique.heuristic import OneHeuristic, \
    ManhattanDistanceHeuristic, CustomHeuristic, PatternDBsHeuristic, Heuristic
from planification_automatique.pddl_problem import PDDLProblem
from planification_automatique.planificateur import Planificateur
from planification_automatique.search_algorithm.a_star import AStar
from planification_automatique.utils import timeout, TimeoutError


@timeout(1200)
def test_one_heuristic(problem: PDDLProblem, heuristic: Heuristic) -> (int, float):
    a_star: AStar = AStar(heuristic)
    planificateur: Planificateur = Planificateur(problem, a_star)
    start: float = time.perf_counter()
    solution, cost, plan = planificateur.solve()
    end: float = time.perf_counter()
    print("=========================================================")
    print(f"Heuristic: {heuristic.__class__.__name__}")
    print("=========================================================")
    if not solution:
        print("No solution found")
        return -1, heuristic.__class__.__name__, end - start

    is_valid_plan: bool = planificateur.verify_solution(plan)
    if not is_valid_plan:
        print("Plan is not correct")
        return -100, heuristic.__class__.__name__, end - start

    print(
        "Solution found with cost {cost} in {plan_size} steps and {time:.2f} seconds"
        .format(cost=cost, plan_size=len(plan), time=end - start)
    )
    print("=========================================================")
    return len(plan), end - start


def test_all_heuristics(problem: PDDLProblem) -> dict:
    one_heuristic: OneHeuristic = OneHeuristic()
    manhattan_distance_heuristic: ManhattanDistanceHeuristic = ManhattanDistanceHeuristic()
    custom_heuristic: CustomHeuristic = CustomHeuristic(problem)
    pattern_dbs_heuristic: PatternDBsHeuristic = PatternDBsHeuristic(problem)
    heuristics: list = [
        one_heuristic,
        manhattan_distance_heuristic,
        custom_heuristic,
        pattern_dbs_heuristic
    ]
    data: dict = {}
    for heuristic in heuristics:
        try:
            plan_size, time_ = test_one_heuristic(problem, heuristic)
            data[heuristic.__class__.__name__] = {
                "plan_size": plan_size,
                "time": time_
            }
        except TimeoutError:
            print("Timeout")
            data[heuristic.__class__.__name__] = {
                "plan_size": "Timeout",
                "time": "Timeout"
            }
        except Exception as _:
            print(
                f"{heuristic.__class__.__name__} doesn't work on {problem.problem.name}")
            data[heuristic.__class__.__name__] = {
                "plan_size": "Error",
                "time": "Error"
            }
    return data


def test_all_problems():
    data: dict = {}
    data_folder: Path = Path("planification_automatique/data")
    for group in range(1, 4):
        group: str = f"groupe{group}"
        for problem_file in (data_folder / group).glob("problem*.pddl"):
            problem: pddl.core.Problem = parse_problem(problem_file)
            problem.domain = parse_domain(problem_file.with_name("domain.pddl"))
            pddl_problem: PDDLProblem = PDDLProblem(problem)

            data[f"{group}_{problem_file.stem}"] = test_all_heuristics(pddl_problem)
            with open("planification_automatique/data/results.json", "w") as f:
                json.dump(data, f, indent=4)


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

    custom_heuristic: CustomHeuristic = CustomHeuristic(problem)
    a_star: AStar = AStar(custom_heuristic)
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

    print(
        "Solution found with cost {cost} in {plan_size} steps and {time:.2f} seconds"
        .format(cost=cost, plan_size=len(plan), time=end - start)
    )
    print("-----------------------------------------")
    print("Found Plan:")
    print("-----------")
    text_plans = " => ".join(
        [f"{action['name']}({', '.join([str(obj) for obj in action['objects']])})" for
         action in plan])
    print(text_plans)
    print("=========================================================")


if __name__ == "__main__":
    main()
