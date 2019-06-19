import random as r
from ConnectFour import *

r.seed(0)


class Node:  # data container
    def __init__(self, parent_node, action, root=False, index=-1):  # a is action
        self.daughters = []
        self.daughter_actions = []
        self.visit_count = 0
        self.value = r.uniform(0, 1.0)
        self.mean_value = 0  # turn into property
        self.action_vector = [r.uniform(0, 1.0) for _ in range(0, 7)]
        self.index = index
        self.taken_action = action
        if root:
            self.board = game.board
            self.parent = None
            self.visit_count = 1
        else:
            self.board = game.generate_node_board(parent_node.board, action)
            self.parent = parent_node.index
            parent_node.daughters.append(self.index)   # use daughter objects instead
            parent_node.daughter_actions.append(self.taken_action)
        self.legal_moves = game.legal_moves(self.board)


class Tree:  # contains all game nodes
    def __init__(self):
        self.root = self._create_root_node()
        self.nodes = []     # stores all nodes, node.index is a node's index in this list

    def _create_root_node(self):
        root = Node(None, None, root=True)
        return root

    def initialize_new_node(self, parent, action):  # creates Node object from another node and an action
        index = len(self.nodes)
        result = Node(parent, action, index=index)
        self.nodes.append(result)

    def is_leaf_node(self, node):
        if len(node.doughters) == 0:
            return True
        else:
            return False

    def QU_factors(self, node):  # returns modified action vector
        result = [0] * 7  # same shape as action vector

        for a in range(0, 7):  # a is an index of an action vector
            if a in node.daughter_actions:
                i = node.daughter_actions.index(a)
                j = node.daughters[i]
                daughter = self.nodes[j]
                result[a] = daughter.mean_value + \
                    (node.action_vector[a] * node.visit_count ** 0.5)/(1 + daughter.visit_count)
            elif a in node.legal_moves:
                result[a] = node.action_vector[a] * node.visit_count ** 0.5
        return result

    def choose_action(self, node):  # returns an index of the action vector as well as the actions already taken
        QU = self.QU_factors(node)
        m = max(QU)
        return QU.index(m)

    def search(self, n):
        for _ in range(0, n):
            esc = False

            current_node = self.root
            a = self.choose_action(current_node)
            print('chosing action %d from the root node...'  %a)

            while a in current_node.daughter_actions:
                print('that action already has a node')
                i = current_node.daughter_actions.index(a)  # simplify later
                j = current_node.daughters[i]
                current_node = self.nodes[j]  # gives the index of the daughter node
                current_node.visit_count += 1
                if len(current_node.legal_moves) == 0:
                    print('escaping')
                    esc = True
                    break
                print('chosing action %s' %a )
                a = self.choose_action(current_node)

            if not esc:
                print('initializing new node from node ID %d and action %d' %(current_node.index, a))
                self.initialize_new_node(current_node, a)



game = Game()
t = Tree()
game.show(t.root.board)


def backpropagate(leaf):  # don't forget about this
    pass


t.search(5)

print(t.QU_factors(t.root))
print(t.root.daughter_actions)

for i in t.root.daughters:
    print(t.nodes[i].visit_count)


'''t.initialize_new_node(t.root, 2)
t.initialize_new_node(t.root, 5)
t.initialize_new_node(t.nodes[0], 4)
t.initialize_new_node(t.nodes[0], 2)

print(t.root.action_vector)
print(t.root.legal_moves)
print(choose_action(t.nodes[2]))'''






