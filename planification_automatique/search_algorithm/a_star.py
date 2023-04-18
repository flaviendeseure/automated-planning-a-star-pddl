import heapq
from typing import AbstractSet

import pddl.logic.base as logic

from planification_automatique.heuristic import Heuristic
from planification_automatique.pddl_problem import PDDLProblem
from planification_automatique.search_algorithm import SearchAlgorithm


class AStar(SearchAlgorithm):
    def __init__(self, heuristic: Heuristic) -> None:
        super().__init__(heuristic)

    def search(self, problem: PDDLProblem) -> (AbstractSet[logic.Formula], int, list):
        open_queue = PriorityQueue()
        closed_set: set = set()
        start: AbstractSet[logic.Formula] = problem.initial_state
        open_queue.put(start, 0)
        g: dict = {
            str(start): self.heuristic(
                state=start,
                goal=problem.goal,
            )
        }
        actions: dict = {str(start): []}

        while not open_queue.empty():
            node_current: AbstractSet[logic.Formula] = open_queue.get()

            if problem.is_goal(node_current):
                return node_current, g[str(node_current)], actions[str(node_current)]

            for action in problem.applicable_actions(node_current):
                node_successor: AbstractSet[logic.Formula] = problem.apply_action(
                    node_current, action
                )
                successor_current_cost: int = g[str(node_current)] + 1
                is_already_visited: bool = str(node_successor) in g
                if is_already_visited:
                    if g[str(node_successor)] <= successor_current_cost:
                        continue
                elif str(node_successor) in closed_set:
                    closed_set.remove(str(node_successor))
                    if g[str(node_successor)] <= successor_current_cost:
                        continue
                    open_queue.put(node_successor, g[str(node_successor)])
                else:
                    open_queue.put(
                        node_successor,
                        successor_current_cost + self.heuristic(
                            state=node_successor,
                            goal=problem.goal,
                        )
                    )

                g[str(node_successor)] = successor_current_cost
                if str(node_successor) not in actions:
                    actions[str(node_successor)] = actions[str(node_current)] + [action]
                elif len(actions[str(node_successor)]) > len(actions[str(node_current)] + [action]):
                    actions[str(node_successor)] = actions[str(node_current)] + [action]

            closed_set.add(str(node_current))

        return None, float("inf")


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]
