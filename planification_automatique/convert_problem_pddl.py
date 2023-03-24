from pddl.logic import Predicate, constants, variables
from pddl.core import Domain, Problem, Action, Requirements
from pddl.formatter import domain_to_string, problem_to_string

def main():
    # set up variables and constants
    x, y, z = variables("x y z", types=["type_1"])
    a, b, c = constants("a b c", types=["type_1"])

    # define predicates
    p1 = Predicate("p1", x, y, z)
    p2 = Predicate("p2", x, y)

    # define actions
    a1 = Action(
        "action-1",
        parameters=[x, y, z],
        precondition=p1(x, y, z) & ~p2(y, z),
        effect=p2(y, z)
    )

    # define the domain object.
    requirements = [Requirements.STRIPS, Requirements.TYPING]
    domain = Domain("my_domain",
        requirements=requirements,
        types=["type_1"],
        constants=[a, b, c],
        predicates=[p1, p2],
        actions=[a1])

    print(domain_to_string(domain))


if __name__ == "__main__":
    main()