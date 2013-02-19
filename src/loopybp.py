#!/usr/bin/env python3

"""
loopy belief propagation on a fully connected graph, assuming binary potentials.
Don't make a cluster graph; just do the BP over the initial Markov network!
Good idea? We'll find out!
"""

## this might be a good thing to do with Cython.

## need to come up with some good data structures for this.

INFINITY = float('inf')
def bp_step():
    ## for every node, calculate that node's outgoing messages. There should be
    ## n-1 of them, for a graph with n nodes.
    for each node:
        for each neighbor:
            sum_penalties = 0
            ## for your value...
            for yourval in your possible values:
                lowest_penalty = INFINITY;

                for myval in my possible values:
                    unary_cost = my unary cost for this value
                    penalty = unary_cost
                    penalty += V(d, your_d)

                    for each neighbor other than the :
                        penalty += previous message from that neighbor to me
                    lowest_penalty = min(penalty, lowest_penalty)

                if (lowest_penalty == INFINITY):
                    print("INFINITE PENALTY")
                output message from me to you[your value] = lowest_penalty
                sum_penalties += lowest_penalty;

            ## now normalize. we want to say that we have a total outgoing
            ## penalty.
            Z = sum_penalties / TOTAL_MSG_PENALTY
            for every element of the message from me to you:
                divide that element by Z

def beliefprop():
    previous_messages = {}
    current_messages = {}

    initialize_messages()

    for step in range(NSTEPS):
        print("beliefprop timestep:", step)
        current_messages = bp_step(previous_messages)
        ## double buffering!!
        previous_messages = current_messages

    ## OK, now let's get the actual best answers.
    for each node:
        for each possible value for that node:
            unary_cost = unary cost for that node for that value
            penalty = unary_cost;
            for each neighbor:
                penalty += that neighbors message to this node[value]
            if (penalty < lowest_penalty):
              lowest_penalty = penalty;
              best_value = value

def main():
    pass

if __name__ == "__main__": main()
