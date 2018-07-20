"""
parameter class object. Specified class to store all model parametes,
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
import LinkService as linkService
from collections import namedtuple
import logging

# logger = logging.getLogger("src.GlobalParameters")


R = 0.25                        # Data rate in bits
Bn = 0.22                       # Noise bandwidth
defaultPower = 0.2              # Transmission power, in watts
whiteNoiseVariance = None
Gt = 1                          # Effective transmitter antenna gain
Gr = 1                          # Effective receiver antenna gain
freq = 2.4e9                    # Transmission frequency, in Hz
lamb = 3e8/freq                 # Wavelength of the transmitted signal, in meters
L = 1                           # System loss factor not related to the propagation
arq = 60                        # File size in bytes
pathLossExp = 2                 # For initial tests, see table in docstring (1.1)
std_db = 0.1                    # Deviation used to calculate path loss
d0 = 1                          # Reference distance for Friss formula
defaultRate = 5e6               # Default transmission rate
limiar_snr = 30                 # SNR upper limit in dB
limiar_snr_delta = 1            # SNR lower limit in dB
limiar_prr = 0                  # Lower PRR limit, where communication is impossible

def setWhiteNoiseVariance():
    Pr = linkService.friss(d0)
    global whiteNoiseVariance
    whiteNoiseVariance = Pr/1e4

def getParametersFromModel(self, model):
    """
    This method allows user to set parameters used for the network model calculation from a predefined model.
    :param model: A transmitter model with predefined configurations.
    :return:  This method returns void.
    """

    self.R = model.R
    self.Bn = model.Bn
    self.Gt = model.G
    self.Gr = model.R
    self.defaultPower = model.transmissionPower
    self.freq = model.freq
    self.lamb = 3e8/self.freq