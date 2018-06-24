"""
Global parameter class object. Specified class to store all model parametes,
such as transmission power and noise floor.
MUST be called in every project file.

"""


class GlobalParameters:

    R = None
    Bn = None
    whiteNoiseVariance =  None
    defaultPower = None
    Gt = None
    Gr = None
    freq = None
    L = None
    ht = None
    hr = None
    pathLossExp = None
    std_db = None
    d0 = None

    def __init__(self):
        pass
