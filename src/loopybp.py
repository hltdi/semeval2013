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
NSTEPS = 2

## this might be a good thing to do with Cython.

## need to come up with some good data structures for this.

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
def unary_potential(name, value):
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
    return edge.potentials[(v1_val, v2_val)]

@lru_cache(maxsize=100)
def get_edge(v1, v2):
    """Return the Edge object for the two named nodes."""
    v1, v2 = sorted([v1, v2])
    return edges[(v1,v2)]

INFINITY = float('inf')

def bp_step(messages):
    ## for every node, calculate that node's outgoing messages. There should be
    ## n-1 of them, for a graph with n nodes.
    return messages

    ## for each node:
    ##     for each neighbor:
    ##         sum_penalties = 0
    ##         ## for your value...
    ##         for yourval in your possible values:
    ##             lowest_penalty = INFINITY;
    ##             for myval in my possible values:
    ##                 unary_cost = my unary cost for this value
    ##                 penalty = unary_cost
    ##                 penalty += V(d, your_d)
    ##                 for each neighbor other than the :
    ##                     penalty += previous message from that neighbor to me
    ##                 lowest_penalty = min(penalty, lowest_penalty)
    ##             if (lowest_penalty == INFINITY):
    ##                 print("INFINITE PENALTY")
    ##             output message from me to you[your value] = lowest_penalty
    ##             sum_penalties += lowest_penalty;
    ##         ## now normalize. we want to say that we have a total outgoing
    ##         ## penalty.
    ##         Z = sum_penalties / TOTAL_MSG_PENALTY
    ##         for every element of the message from me to you:
    ##             divide that element by Z


def initialize_messages(nodes):
    """Produce an initial setting for the messages."""
    messages = {}
    for fromnode in nodes.keys():
        for tonode in nodes.keys():
            msg = {}
            for val in possible_values(tonode):
                msg[val] = 1 / TOTAL_MSG_PENALTY
            messages[(fromnode,tonode)] = msg
    return messages

## a message is just a unary factor.
## looks like {'value': penalty, ...}
## current_messages is a map like: {(from, to): message, ...}

def beliefprop():
    previous_messages = {}
    current_messages = None

    previous_messages = initialize_messages(nodes)

    for step in range(NSTEPS):
        print("beliefprop timestep:", step)
        current_messages = bp_step(previous_messages)
        ## double buffering!!
        previous_messages = current_messages

    ## OK, now let's get the actual best answers.
    ## for each node:
    ##     for each possible value for that node:
    ##         unary_cost = unary cost for that node for that value
    ##         penalty = unary_cost;
    ##         for each neighbor:
    ##             penalty += that neighbors message to this node[value]
    ##         if (penalty < lowest_penalty):
    ##           lowest_penalty = penalty;
    ##           best_value = value

def main():
    a = Node('a', {'a1': 10, 'a2': 5})
    b = Node('b', {'b1': 9, 'b2': 5})

    edgepotentials = {('a1','b1'):2,
                      ('a1','b2'):10,
                      ('a2','b1'):10,
                      ('a2','b1'):10,
                     }
    e1 = Edge('a', 'b', edgepotentials)

    e2 = get_edge('b', 'a')
    print(e1, e2, e1 == e2)
    print(get_edge_penalty('a', 'a1', 'b', 'b2'))


    print(initialize_messages(nodes))

if __name__ == "__main__": main()
