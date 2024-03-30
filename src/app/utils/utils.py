from itertools import filterfalse, tee
from typing import Iterable


def identity(value: any):
    return value


def partition(iterable: Iterable, pred: callable = identity):
    t1, t2 = tee(iterable)
    t, f = filter(pred, t1), filterfalse(pred, t2)
    return list(t), list(f)
