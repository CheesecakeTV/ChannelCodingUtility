import numpy as np
from scipy.special import binom
from typing import Iterator
from itertools import count

def probability_k_errors(errorRate:float|np.ndarray,n:int|np.ndarray,k:int|np.ndarray) -> float|np.ndarray:
    """
    Returns the probability of exactly k errors happening in n symbols.
    You can replace ONE parameter by a np.ndarray.
    :param errorRate: 0 - 1, single symbol error probability
    :param n: Symbol count
    :param k: Error count
    :return: 0 - 1
    """
    try:
        return binom(n,k) * (errorRate ** k) * ((1 - errorRate) ** (n - k))
    except OverflowError:
        return errorRate * 0 + n * 0 + k * 0 # When you pass arrays, this will be converted to array

def probability_k_range(
        errorRate:float|np.ndarray,
        n:int|np.ndarray,
        k_min:int = 0,
        k_max:int = -1,
        returnKAsTuple:bool=False
) -> Iterator[float|np.ndarray|tuple[int|float]|tuple[int|np.ndarray]]:
    """
    Returns values of probability_k_errors while increasing k from 0 to k_max.
    :param returnKAsTuple: True, if k should also be returned
    :param k_min: First k to be returned
    :param k_max: Last k to be returned. -1 will make it run forever.
    :param errorRate: 0 - 1, single symbol error probability
    :param n: Symbol count
    :return: (k, probability) or (probability) depending on returnKAsTuple
    """
    for k in count(k_min):
        _ = probability_k_errors(errorRate,n,k)
        if returnKAsTuple:
            yield k,_
        else:
            yield _

        if k == k_max:
            return

def get_table(
        errorRate: float | np.ndarray,
        n: int | np.ndarray,
        k_max: int,
        k_min: int = 0,
        rounding = 100,
        to_array:bool = False,
) -> list[list] | np.ndarray:
    """
    Creates a Table suited for the sg.table in main layout

    A "table row" contains the following:
        k:          Error count
        P(k):       Probability of k errors
        P(<=k):     Probability of up to k errors
        P(>k):      Probability of more than k errors
        1 // P(>k): Rough estimate of how frequently an n-sized block of symbols will have more than k errors. 'How many transmissions until the next error?'

    :param to_array: True, if return should be converted to np.array
    :param rounding: How many decimal points to be rounded to
    :param errorRate: Single Symbol error probability
    :param n: Number of samples
    :param k_min: first k to be considered
    :param k_max: last k to be considered
    :return: (Detailed description in docstring)
    """

    cum_sum = 0
    table = list()
    for k, P in probability_k_range(errorRate, n, k_min, k_max, returnKAsTuple=True):
        cum_sum += P

        if isinstance(P,np.ndarray):
            k = np.full_like(P,k)
            cum_sum = np.clip(cum_sum,0,1)
        else:
            cum_sum = min(1,cum_sum)
        try:
            table.append([
                k,
                np.round(P, rounding),
                np.round(cum_sum, rounding),
                np.round(1 - cum_sum, rounding),
                np.round(1 / (1 - cum_sum))
            ])
        except ZeroDivisionError:
            continue

    if to_array:
        return np.array(table)
    return table




