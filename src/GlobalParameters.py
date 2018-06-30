"""
Global parameter class object. Specified class to store all model parametes,
such as transmission power and noise floor.
MUST be called in every project file.

================================================================================
1. CONSIDERATIONS
1.1 Path Loss Exp

-------------------------------------------------------
|         ENVIRONMENT           | PATH LOSS EXPONENT  |
-------------------------------------------------------
| Free Space                    |           2         |
| Urban area cellular radio     |       2.7 to 3.5    |
| Shadowed urban cel radio      |         3 to 5      |
| Inside a building             |       1.6 to 1.8    |
| Obstructed in building        |         4 to 6      |
| Obstructed in factory         |         2 to 3      |
-------------------------------------------------------


"""
import src.LinkService as linkService
import logging

# logger = logging.getLogger("src.GlobalParameters")

class GlobalParameters:

    R = None
    Bn = None
    whiteNoiseVariance = None
    defaultPower = 0.2              # Transmission power
    Pr = None                       # Received power available
    Gt = 1                          # Effective transmitter antenna gain
    Gr = 1                          # Effective receiver antenna gain
    freq = 2.4e9                    # Transmission frequency
    lamb = 3e8/freq                 # Wavelength of the transmitted signal
    L = 1                           # System loss factor not related to the propagation
    ht = 1
    hr = 1
    pathLossExp = 2
    std_db = 0.1
    d0 = 1
    defaultRate = 5e6
    limiar_snr = 30
    limiar_snr_delta = 1

    def __init__(self):
        pass

    def initialize(self):
        self.Pr = linkService.friss(self.defaultPower, self.Gt, self.Gr, self.lamb, self.d0, self.L)
        self.setWhiteNoiseVariance()
        # logger.info("Initialized global parameters: ", self)


    def setWhiteNoiseVariance(self):
        self.whiteNoiseVariance = self.Pr/1e4
