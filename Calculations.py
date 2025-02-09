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

def ber_from_ser(ser:float|np.ndarray,bit_per_symbol:int = 8) -> float|np.ndarray:
    """
    Calculates the bit-error-rate (BER) based on the symbol-error-rate (SER) and the bit-count per symbol.
    It's easier to measure SER, but sometimes you want to know BER
    :param ser: Symbol error rate
    :param bit_per_symbol: How many bits per symbol (Usually 8)
    :return: Bit error rate
    """
    assert bit_per_symbol, "bit_per_symbol can't be 0"
    return 1 - ((1 - ser) ** (1/bit_per_symbol))

def ser_from_ber(ber:float|np.ndarray,bit_per_symbol:int = 8) -> float|np.ndarray:
    """
    Calculates the symbol-error-rate (SER) based on the bit-error-rate (BER) and the bit-count per symbol.
    :param ber: Symbol error rate
    :param bit_per_symbol: How many bits per symbol (Usually 8)
    :return: Bit error rate
    """
    assert bit_per_symbol, "bit_per_symbol can't be 0"
    return 1 - (1 - ber) ** bit_per_symbol

@np.vectorize
def round_to_exponential(x:float,digits:int = 2) -> float:
    """
    Rounds relative to the first non-zero digit.
    Perfect to use when formatting to exponentials like e.g. 5.02e-6
    :param x: Number to be rounded
    :param digits: How many digits AFTER the first one. 0 means, only keep first digit.
    :return: Rounded float
    """
    if x == 0:
        return 0
    exp = int(np.log10(x))
    return np.round(x,-exp + 1 + digits)




