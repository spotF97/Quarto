from abstract.state import State



class Node:
    def __init__(self, state: State):
        self.state = state

    @classmethod
    def evaluate(cls, state, depth_limit=0):
        if depth_limit == 0:
            return 0, None

        if state.is_lose():
            return -1, None
        elif state.is_draw():
            return 0, None
        else:
            return 1, None
