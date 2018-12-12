import numpy as np
from scipy import special


def part(n, m, _lambda):

    chance = (1 - 1 / n) ** (n - 1) if n > 0 else 1

    if n < 2:
        return _lambda**(m) / special.factorial(m) * np.exp(-_lambda)

    elif n > m:
        return chance * np.exp(-_lambda)

    else:

        a = chance * _lambda**(m-n+1) / special.factorial(m-n+1) * np.exp(-_lambda)
        b = (1-chance) * _lambda**(m-n) / special.factorial(m-n) * np.exp(-_lambda)
        return a + b


def theory(_lambda, moments):

    A = np.zeros((moments, moments))
    for m in range(moments-1):
        for n in range(m+2):
            A[m][n] = part(n, m, _lambda)

    A = A - np.eye(moments)
    A[-1][:] = 1

    B = np.zeros((moments, 1))
    B[-1][0] = 1

    P = np.dot(np.linalg.inv(A), B)
    return np.sum(np.transpose(P) * np.arange(0, moments))
