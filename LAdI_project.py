import networkx as nx
import matplotlib.pyplot as plt

OPERATORS = set(['+', '-', '*', '/', '(', ')', '^'])  # set of operators


class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[self.size() - 1]

    def size(self):
        return len(self.items)


class InfixConverter:
    def __init__(self):
        self.stack = Stack()
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

    def has_less_or_equal_priority(self, a, b):
        if a not in self.precedence:
            return False
        if b not in self.precedence:
            return False
        return self.precedence[a] <= self.precedence[b]

    def is_operator(self, x):
        ops = ['+', '-', '/', '*']
        return x in ops

    def is_operand(self, ch):
        return ch.isalpha() or ch.isdigit()

    def is_open_parenthesis(self, ch):
        return ch == '('

    def is_close_parenthesis(self, ch):
        return ch == ')'

    def to_postfix(self, expr):
        expr = expr.replace(" ", "")
        self.stack = Stack()
        output = ''

        for c in expr:
            if self.is_operand(c):
                output += c
            else:
                if self.is_open_parenthesis(c):
                    self.stack.push(c)
                elif self.is_close_parenthesis(c):
                    operator = self.stack.pop()
                    while not self.is_open_parenthesis(operator):
                        output += operator
                        operator = self.stack.pop()
                else:
                    while (not self.stack.is_empty()) and self.has_less_or_equal_priority(c, self.stack.peek()):
                        output += self.stack.pop()
                    self.stack.push(c)

        while not self.stack.is_empty():
            output += self.stack.pop()
        return output


class Node:
    # Constructor to create a node
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def is_operator(char):
    return char in OPERATORS


def in_order(t):
    if t is not None:
        in_order(t.left)
        print(t.value)
        in_order(t.right)


def construct_tree(postfix, filename):
    graph = nx.DiGraph()
    stack = []
    current_top = 0
    labels = {}
    # Traverse through every character of input expression
    for char in postfix:

        # if operand, simply push into stack
        if not is_operator(char):
            t = Node(char)
            stack.append(t)

        # Operator
        else:

            # Pop two top nodes
            t = Node(char)
            t1 = stack.pop()
            t2 = stack.pop()
            graph.add_edge(current_top+2, current_top+1)
            graph.add_edge(current_top + 2, current_top)

            # make them children
            t.right = t1
            t.left = t2

            labels[current_top] = t1.value
            labels[current_top+1] = t2.value
            current_top += 2

            # Add this subexpression to stack
            stack.append(t)

    # Only element  will be the root of expression tree
    plt.figure(dpi=300)
    t = stack.pop()
    labels[current_top] = t.value
    pos = nx.circular_layout(graph)
    nx.draw(graph, node_size=100, pos=pos, with_labels=False)
    nx.draw_networkx_labels(graph, pos, labels)
    plt.savefig(f'{filename}.png')

    return t


def expr(n):
    if n < 2:
        if n == 1:
            return ["(v*t + x)", "(V*t + X)"]
        return ["x", "X"]

    x1k = expr(n-2)[0]
    x2k = expr(n-2)[1]
    x1kplus1 = expr(n-1)[0]
    x2kplus1 = expr(n-1)[1]

    return [f"((t^2*q*Q)/(4*p*E*({x1k}-{x2k}))-{x1k}+2*{x1kplus1})", f"((-t^2*q*Q)/(4*p*E*({x1k}-{x2k}))-{x2k}+2*{x2kplus1})"]


def main():
    converter = InfixConverter()
    f = open("result.txt", "w")
    for i in range(7):
        result = expr(i)
        if 4 > i > 0:
            postfix = converter.to_postfix(result[0])
            filename = f"tree{i}"
            construct_tree(postfix, filename)
        f.write(f"x1{i} = {result[0]}\n")
        f.write(f"x2{i} = {result[1]}\n")
    f.close()


if __name__ == "__main__":
    main()
