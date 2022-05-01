from typing import Iterator, Any
from functools import reduce
import operator


def prod(iterable: Iterator[Any]):
    return reduce(operator.mul, iterable, 1)
