from pathlib import Path

from pddl import parse_domain, parse_problem


def main():
    folder = Path("planification_automatique/pddl")
    domain = parse_domain(folder / "domain.pddl")
    print(domain)

    problem = parse_problem(folder / "problem1.pddl")
    print(problem)
    problem_2 = parse_problem(folder / "problem2.pddl")
    print(problem_2)


if __name__ == "__main__":
    main()
