import dataclasses
from mini_max.node import Node

""" αβウィンドウ """
@dataclasses.dataclass(frozen=True)
class Window:
    alpha: float = -float('inf')
    beta: float = float('inf')


class MiniMax:

    @classmethod
    def nega_max(cls, node: Node, depth_limit, window):

        # 深さ制限に到達 or 決着したら
        """
        if state.is_done():
            if state.is_lose():
                return depth_limit*10 - 200, None
            elif state.is_draw():
                return 0, None
            else:
                return 200 - depth_limit*10, None

        if depth_limit == 0:
            return cls.evaluate(state), None
        """

        if node.state.is_done() or depth_limit == 0:
            return node.evaluate(node.state, depth_limit), None


        v = -float('inf')
        best_action = None
        for action in node.state.legal_actions():

            child_state = node.state.next(action)
            child_node = Node(state=child_state)

            temp_v, _ = MiniMax.nega_max(child_node, depth_limit-1, Window(alpha=-window.beta, beta=-window.alpha))
            temp_v = temp_v * -1
            if temp_v >= v:
                v = temp_v
                best_action = action

            if v >= window.beta:
                return v, best_action

            if v > window.alpha:
                window.alpha = v

        return v, best_action


    @classmethod
    def nega_max_select_action(cls, node: Node, depth):
        _, action = cls.nega_max(node, depth, Window())
        return action
