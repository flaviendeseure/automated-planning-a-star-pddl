import heapq

from planification_automatique.pddl_problem import PDDLProblem


class Planificateur:
    def __init__(self, problem: PDDLProblem, search_algorithm, heuristic) -> None:
        self.problem = problem
        self.search_algorithm = search_algorithm
        self.heuristic = heuristic

    def solve(self):
        pass


# Classe pour implémenter une file d'attente de priorité
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


# Fonction pour implémenter l'algorithme A* pour la recherche
def a_star_search(problem):
    frontier = PriorityQueue()
    start = problem.initial_state()
    frontier.put(start, 0)
    cost_so_far = {start: 0}

    while not frontier.empty():
        current = frontier.get()

        if problem.is_goal(current):
            return current, cost_so_far[current]

        for action in problem.actions(current):
            next_state = problem.result(current, action)
            new_cost = cost_so_far[current] + 1
            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                cost_so_far[next_state] = new_cost
                priority = new_cost + problem.heuristic(next_state)
                frontier.put(next_state, priority)

    return None, float("inf")
