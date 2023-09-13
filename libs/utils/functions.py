from dreal import *
import torch
import numpy as np


def EXCheckLyapunov(x, f, V, config, excheck):
    if len(x) == 2:
        ball_x1 = Expression(0)
        ball_x2 = Expression(0)
        ball_x1 += x[0]
        ball_x2 += x[1]
        lie_derivative_of_V = Expression(0)
        for i in range(len(x)):
            lie_derivative_of_V += f[i] * V.Differentiate(x[i])
        ball_in_bound = logical_and(excheck[0].lb() <= ball_x1, ball_x1 <= excheck[0].ub(), excheck[1].lb() <= ball_x2, ball_x2 <= excheck[1].ub())
    else:
        raise NotImplementedError

    # Constraint: Lie derivative of V <= 0)
    condition = logical_and(ball_in_bound, lie_derivative_of_V > 0)
    check = CheckSatisfiability(condition, config)
    return check, lie_derivative_of_V