import random
from typing import Callable
import numpy as np
import heapq


class State:
    def __init__(self, data: np.ndarray):
        self._data = data.copy()
        self._data.flags.writeable = False

    def __hash__(self):
        return hash(bytes(self._data))

    def __eq__(self, other):
        return bytes(self._data) == bytes(other._data)

    def __lt__(self, other):
        return bytes(self._data) < bytes(other._data)

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return repr(self._data)

    @property
    def data(self):
        return self._data

    def copy_data(self):
        return self._data.copy()

class PriorityQueue:
    """A basic Priority Queue with simple performance optimizations"""

    def __init__(self):
        self._data_heap = list()
        self._data_set = set()

    def __bool__(self):
        return bool(self._data_set)

    def __contains__(self, item):
        return item in self._data_set

    def push(self, item, p=None):
        assert item not in self, f"Duplicated element"
        if p is None:
            p = len(self._data_set)
        self._data_set.add(item)
        heapq.heappush(self._data_heap, (p, item))

    def pop(self):
        p, item = heapq.heappop(self._data_heap)
        self._data_set.remove(item)
        return item

def goal_test(N, state):
    return state == set(range(N))

def search(N, lists, parent_state: dict, state_cost: dict, priority_function: Callable):
    parent_state.clear()
    state_cost.clear()
    state = State(np.array(set()))
    parent_state[state] = None
    state_cost[state] = 0
    numOfNodes = 0
    numOfElements = 0
    frontier = PriorityQueue()
    s = state.copy_data()
    
    while(state is not None and not goal_test(N, s)):
        for a in range(len(lists)):
            newState = s
            cost = 0
            if not set(lists[a]) < s:
                newState = s | set(lists[a])
                cost = len(lists[a])
            new = State(np.array(newState))
            if new not in state_cost and new not in frontier:
                parent_state[new] = state
                state_cost[new] = state_cost[state] + cost
                frontier.push(new, p=priority_function(newState))
            elif new in frontier and state_cost[new] > state_cost[state] + cost:
                parent_state[new] = state
                state_cost[new] = state_cost[state] + cost
            if goal_test(N, newState):
                break
        
        if frontier:
            state = frontier.pop()
            numOfElements = state_cost[state]
            numOfNodes += 1 
        else:
            state = None
            numOfElements = 0
            numOfNodes = 0
        s = state.copy_data()
        
    return numOfElements, numOfNodes

def problem(N, seed=None):
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]
    

if __name__ == "__main__":
    for N in [5, 10, 20, 100, 500, 1000]:
        lists = problem(N, 42)
        parent_state = dict()
        state_cost = dict()
        numOfElements, numOfNodes = search(N, lists, parent_state=parent_state, state_cost=state_cost, priority_function=lambda s: (-len(s), state_cost[State(np.array(s))]))
        print(f"For N = {N}: number of elements = {numOfElements}, number of nodes = {numOfNodes}")
    
