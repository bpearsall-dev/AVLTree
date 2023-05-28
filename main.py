import networkx as nx
import matplotlib.pyplot as plt
import os
import pydot
from IPython.display import Image, display


# Node class for AVL Tree
class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


# AVL Tree Class
class AVLTree:
    def __init__(self):
        self.root = None
        self.rotation_needed = False
        self.rotation_type = None
        self.heaviness = None

    # Method to calculate balance of a node
    def _balance(self, node):
        if not node:
            return 0
        return self._height(node.left) - self._height(node.right)

    # Method to find the maximum key in a subtree
    def _find_max(self, node):
        if node.right:
            return self._find_max(node.right)
        return node

    # Method to insert a node into the AVL Tree
    def insert(self, key):
        print(f"Inserting node {key}")
        self.root = self._insert(self.root, key)
        if self.rotation_needed:
            if self.heaviness == "L" and self.rotation_type == "right":
                rotation_info = "Double rotation - Left right rotation (LR)"
                node_heaviness = "left"
            elif self.heaviness == "R" and self.rotation_type == "right":
                rotation_info = "Double rotation - Right left rotation (RL)"
                node_heaviness = "right"
            elif self.heaviness == "L" and self.rotation_type == "left":
                rotation_info = "Single rotation - Left rotation (LL)"
                node_heaviness = "left"
            elif self.heaviness == "R" and self.rotation_type == "left":
                rotation_info = "Single rotation - Right rotation (RR)"
                node_heaviness = "right"
            elif self.rotation_type == "right-left":
                rotation_info = "Double rotation - Right left rotation (RL)"
                node_heaviness = "right"
            elif self.rotation_type == "left-right":
                rotation_info = "Double rotation - Left right rotation (LR)"
                node_heaviness = "left"
            print(
                f"Rotation needed: {rotation_info} due to node {node_heaviness} heavy with a balance factor of {self._balance_factor(self.root)}")
            print("After rotation:")
        else:
            print("No rotation required")
        self.print_node_degrees()
        self.display_and_plot(pos={})

    # Method to remove a node from the AVL Tree
    def remove(self, key):
        print(f"Removing node {key}")
        self.root = self._remove(self.root, key)
        self.print_node_degrees()
        self.display_and_plot(pos={})

    def _get_all_nodes(self, node):
        if not node:
            return []
        return [node] + self._get_all_nodes(node.left) + self._get_all_nodes(node.right)

    def _get_all_balance_factors(self, node):
        if not node:
            return []
        return [self._balance_factor(node)] + self._get_all_balance_factors(node.left) + self._get_all_balance_factors(
            node.right)

    def print_node_degrees(self):
        nodes = self._get_all_nodes(self.root)
        degrees = [self._degree(node) for node in nodes]
        degree_str = ', '.join(f"{node.key}({degree})" for node, degree in zip(nodes, degrees))
        print("Node Degrees:", degree_str)

    def _degree(self, node):
        if node is None:
            return 0
        degree = 0
        if node.left:
            degree += 1
        if node.right:
            degree += 1
        return degree

    # Method to insert a node into the AVL Tree
    def _insert(self, node, key):
        if not node:
            return AVLNode(key)

        elif key < node.key:
            node.left = self._insert(node.left, key)

        else:
            node.right = self._insert(node.right, key)

        node.height = 1 + max(self._height(node.left), self._height(node.right))
        balance = self._balance(node)

        # Left heavy
        if balance > 1:
            if key < node.left.key:
                print(
                    f"Rotation needed: Single right rotation (LL) due to node {node.key} being left heavy with a balance factor of {balance}")
                self.display_and_plot(before_rotation=True)
                return self._right_rotate(node)
            else:
                print(
                    f"Rotation needed: Double rotation - Left right rotation (LR) due to node {node.key} being left heavy with a balance factor of {balance}")
                self.display_and_plot(before_rotation=True)
                node.left = self._left_rotate(node.left)
                return self._right_rotate(node)
        elif balance < -1:
            if key > node.right.key:
                print(
                    f"Rotation needed: Single left rotation (RR) due to node {node.key} being right heavy with a balance factor of {balance}")
                self.display_and_plot(before_rotation=True)
                return self._left_rotate(node)
            else:
                print(
                    f"Rotation needed: Double rotation - Right left rotation (RL) due to node {node.key} being right heavy with a balance factor of {balance}")
                self.display_and_plot(before_rotation=True)
                node.right = self._right_rotate(node.right)
                return self._left_rotate(node)

        return node

    # Method that carries out removal operations and balances the tree
    def _remove(self, node, key):
        if not node:
            return node

        if key < node.key:
            node.left = self._remove(node.left, key)
        elif key > node.key:
            node.right = self._remove(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self._find_max(node.left)
            node.key = temp.key
            node.left = self._remove(node.left, temp.key)

        node.height = 1 + max(self._height(node.left), self._height(node.right))
        balance_factor = self._balance(node)

        # Left heavy
        if balance_factor > 1:
            if self._balance(node.left) >= 0:
                print(
                    f"Rotation needed: Single right rotation (LL) due to node {node.key} being left heavy with a balance factor of {balance_factor}")
                return self._right_rotate(node)
            else:
                print(
                    f"Rotation needed: Double rotation - Left right rotation (LR) due to node {node.key} being left heavy with a balance factor of {balance_factor}")
                node.left = self._left_rotate(node.left)
                return self._right_rotate(node)
        # Right heavy
        elif balance_factor < -1:
            if self._balance(node.right) <= 0:
                print(
                    f"Rotation needed: Single left rotation (RR) due to node {node.key} being right heavy with a balance factor of {balance_factor}")
                return self._left_rotate(node)
            else:
                print(
                    f"Rotation needed: Double rotation - Right left rotation (RL) due to node {node.key} being right heavy with a balance factor of {balance_factor}")
                node.right = self._right_rotate(node.right)
                return self._left_rotate(node)

        return node


    # Method to find the minimum key in a subtree
    def _find_min(self, node):
        if node.left is None:
            return node
        else:
            return self._find_min(node.left)

    # Method to display the AVL tree and plot the nodes
    def display_and_plot(self, node=None, level=0, G=None, pos=None, before_rotation=True):
        if G is None:
            G = nx.DiGraph()
        if pos is None:
            pos = {}
        if node is None:
            node = self.root

        if node.left:
            G.add_edge(node.key, node.left.key)
            pos = self.display_and_plot(node.left, level + 1, G, pos, before_rotation)

        G.add_node(node.key, balance=f"{node.key}({self._balance_factor(node)})")

        if node.right:
            G.add_edge(node.key, node.right.key)
            pos = self.display_and_plot(node.right, level + 1, G, pos, before_rotation)

        if node:
            pos[node.key] = (node.key, 10 - level)

        if level == 0:
            fig, ax = plt.subplots(figsize=(20, 10))
            nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=2500, font_size=12, font_weight="bold",
                    ax=ax)
            labels = nx.get_node_attributes(G, 'balance')
            offset = 0.4
            offset_pos = {k: (v[0], v[1] + offset) for k, v in pos.items()}
            nx.draw_networkx_labels(G, offset_pos, labels, font_color="red", font_size=12, font_weight="bold")

            #  if before_rotation:
            #   plt.title("Before Rotation")
            #   else:
            #   plt.title("After Rotation")
            plt.show()

        return pos

    # Method to calculate the height of a node
    def _height(self, node):
        if not node:
            return 0
        return node.height

    # Method to perform a left rotation at a node
    def _left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self._height(z.left), self._height(z.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))

        return y

    # Method to perform a right rotation at a node
    def _right_rotate(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self._height(y.left), self._height(y.right))
        x.height = 1 + max(self._height(x.left), self._height(x.right))

        return x

    # Method to compute balance factor of a node
    def _balance_factor(self, node):
        return 0 if node is None else self._height(node.left) - self._height(node.right)


# User interface for interacting with the AVL tree
avl = None

while True:
    print("\nOptions:")
    print("1. Create AVL tree")
    print("2. Insert a node")
    print("3. Remove a node")
    print("4. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        avl = AVLTree()
        nodes = input("Enter the nodes (comma-separated): ").split(",")
        for node in nodes:
            avl.insert(int(node))
        print("AVL tree created.")
        avl.print_node_degrees()
        avl.display_and_plot()
    elif choice == 2:
        if not avl:
            print("Please create an AVL tree first.")
        else:
            value = int(input("Enter the value to insert: "))
            avl.insert(value)
    elif choice == 3:
        if not avl:
            print("Please create an AVL tree first.")
        else:
            value = int(input("Enter the value to remove: "))
            avl.remove(value)
    elif choice == 4:
        break
    else:
        print("Invalid choice. Please try again.")
