#!/usr/bin/env python3

"""
loopy belief propagation on a fully connected graph, assuming binary potentials.
Don't make a cluster graph; just do the BP over the initial Markov network!
Good idea? We'll find out!
"""

from functools import lru_cache
from operator import itemgetter

## TUNABLE PARAMETERS (tune it up) ##
TOTAL_MSG_PENALTY = 100

## this might be a good thing to do with Cython.

## two kinds of potentials: unary potentials and binary potentials. we want to
## minimize the potentials over the whole graph.
nodes = {}
class Node:
    def __init__(self, name, potentials):
        """values should be the set of values that this node can take.
        potentials should be a map from the values to a >0 penalty"""
        self.name = name
        self.potentials = potentials
        nodes[name] = self

@lru_cache(maxsize=100)
def get_node_penalty(name, value):
    return nodes[name].potentials[value]

@lru_cache(maxsize=100)
def possible_values(name):
    return set(nodes[name].potentials.keys())

edges = {}
class Edge:
    def __init__(self, v1, v2, potentials):
        """v1 and v2 are edge names."""
        self.v1, self.v2 = sorted([v1, v2])
        self.potentials = potentials

        v1, v2 = sorted([v1, v2])
        edges[(v1,v2)] = self

@lru_cache(maxsize=100)
def get_edge_penalty(v1, v1_val, v2, v2_val):
    edge = get_edge(v1, v2)
    if v1 < v2:
        return edge.potentials[(v1_val, v2_val)]
    else:
        return edge.potentials[(v2_val, v1_val)]

@lru_cache(maxsize=100)
def get_edge(v1, v2):
    """Return the Edge object for the two named nodes."""
    v1, v2 = sorted([v1, v2])
    return edges[(v1,v2)]

INFINITY = float('inf')

def bp_step(prev_messages):
    ## for every node, calculate that node's outgoing messages. There should be
    ## n-1 of them, for a graph with n nodes.
    messages = {}
    nodeset = set(nodes.keys())
    for fromnode in nodeset:
        for tonode in nodeset - set([fromnode]):
            msg = {}
            sum_penalties = 0
            for yourval in possible_values(tonode):
                lowest_penalty = INFINITY
                for myval in possible_values(fromnode):
                    penalty = get_node_penalty(fromnode, myval)
                    penalty += get_edge_penalty(fromnode,myval,tonode,yourval)
                    for neighbor in nodeset - set([fromnode,tonode]):
                        penalty += prev_messages[(neighbor, fromnode)][myval]
                    lowest_penalty = min(penalty, lowest_penalty)
                if (lowest_penalty == INFINITY):
                    print("INFINITE PENALTY")
                msg[yourval] = lowest_penalty
                sum_penalties += lowest_penalty
            ## now normalize. we want to say that we have a total outgoing
            ## penalty.
            Z = sum_penalties / TOTAL_MSG_PENALTY
            for yourval in possible_values(tonode):
                msg[yourval] /= Z
            messages[(fromnode,tonode)] = msg
    return messages

def initialize_messages(nodes):
    """Produce an initial setting for the messages."""
    messages = {}
    nodeset = set(nodes.keys())
    for fromnode in nodeset:
        for tonode in nodeset - set([fromnode]):
            msg = {}
            for val in possible_values(tonode):
                msg[val] = 1 / TOTAL_MSG_PENALTY
            messages[(fromnode,tonode)] = msg
    return messages

## a message is just a unary factor.
## looks like {'value': penalty, ...}
## current_messages is a map like: {(from, to): message, ...}

def beliefprop(NSTEPS):
    """Do BP on the network. Return two values: a dictionary from node names to
    the one-best answer for that node, and a dictionary from node names to the
    top 5 answers for that node."""
    previous_messages = {}
    current_messages = None
    previous_messages = initialize_messages(nodes)

    for step in range(NSTEPS):
        ## print("beliefprop timestep:", step)
        current_messages = bp_step(previous_messages)
        ## double buffering!!
        previous_messages = current_messages

    ## OK, now let's get the actual best answers.
    best_values = {}
    topfive_values = {}
    nodeset = set(nodes.keys())
    for node in nodeset:
        best_value = None
        lowest_penalty = INFINITY

        vp_pairs = []
        for myval in possible_values(node):
            penalty = get_node_penalty(node, myval)
            for neighbor in nodeset - set([node]):
                penalty += current_messages[(neighbor, node)][myval]
            vp_pairs.append((myval, penalty))
            if (penalty < lowest_penalty):
              lowest_penalty = penalty
              best_value = myval
        best_values[node] = best_value
        vp_pairs.sort(key=itemgetter(1), reverse=True)
        topfive_values[node] = [val for (val,penalty) in vp_pairs[:5]]
    return best_values, topfive_values

def main():
    a = Node('a', {'a1': 10, 'a2': 5})
    b = Node('b', {'b1': 9, 'b2': 5})

    edgepotentials = {('a1','b1'):2,
                      ('a1','b2'):10,
                      ('a2','b1'):2,
                      ('a2','b2'):10,
                     }
    e1 = Edge('a', 'b', edgepotentials)
    best_values, top_values = beliefprop(10)
    print(best_values)
    print(top_values)

if __name__ == "__main__": main()
