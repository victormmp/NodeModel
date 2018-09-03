from collections import namedtuple

dim = namedtuple("dim",["start", "end"])
area = namedtuple("area", ["top_left", "botom_right"])

N1_DIM = dim(start=(0.0, 0.0), end=(0.0, 10.0))
N2_DIM = dim(start=(0.0, 0.0), end=(10.0, 10.0))
N3_DIM = dim(start=(0.0, 0.0), end=(0.0, 10.0))

N4_DIM = area(top_left=(0.0, 0.0), botom_right=(10.0, 10.0))
