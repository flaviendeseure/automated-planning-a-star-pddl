import heapq
from pddl import parse_domain, parse_problem


# Classe pour représenter un problème PDDL
class PDDLProblem:
    
    def __init__(self, domain_file, problem_file):
        self.domain = parse_domain(domain_file)
        self.problem = parse_problem(problem_file)

    def initial_state(self):
        return self.problem['init']

    def is_goal(self, state):
        return state.contains(self.problem['goal'])

    def heuristic(self, state):
        # Implémentez votre heuristique ici, si nécessaire.
        # Dans ce cas, nous utilisons une heuristique nulle (0) par défaut.
        return 0

    def actions(self, state):
        # Implémentez une méthode pour renvoyer les actions applicables étant donné un état
        pass

    def result(self, state, action):
        # Implémentez une méthode pour renvoyer l'état résultant après l'application d'une action
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



def main():
    domain_file = 'domain.pddl'
    problem_file = 'problem1.pddl'

    problem = PDDLProblem(domain_file, problem_file)
    solution, cost = a_star_search(problem)

    if solution is not None:
        print(f'Solution found with cost {cost}')
        print(solution)
    else:
        print('No solution found')

if __name__ == '__main__':
    main()
