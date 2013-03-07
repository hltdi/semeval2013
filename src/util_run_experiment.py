def output_one_best(problem, target, solution):
    """Return output for a solution for the one-best."""
    return "{0}.{1} {2} :: {3};".format(problem.source_lex,
                                        target,
                                        problem.instance_id,
                                        solution)
