"""
Parameter class object. Specified class to store all model parameters,
such as transmission power and noise floor.
MUST be imported in every project file.

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
import RadioModels
import numpy as np
from collections import namedtuple
import logging
from settings import *

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
    

def setTransmissionPowerVariance(variance=None):
    global defaultPower
    global USE_TRANSMISSION_POWER_VARIANCE
    
    if (variance==None):
        # Using a default variance for transmission power of 1%
        variance = 0.01 * defaultPower
    if(USE_TRANSMISSION_POWER_VARIANCE):
        defaultPower = defaultPower + np.random.normal(loc=0, scale=variance)
    
    
def initializeGlobalParameters(model):
    getParametersFromModel(model)
    setWhiteNoiseVariance()
    setTransmissionPowerVariance()
    

def getParametersFromModel(model):
    """
    This method allows user to set parameters used for the network model
    calculation from a predefined model.
    :param model: A transmitter model with predefined configurations.
    :return:  This method returns void.
    """

    if model is None:
        print("No model selected.")
        return False
    elif type(model) is not RadioModels.RadioModel:
        raise TypeError("Model is not a valid RadioModel object.")

    global R, Bn, Gt, Gr, defaultPower, freq, lamb, arq

    R = model.R
    Bn = model.Bn
    Gt = model.Gt
    Gr = model.Gr
    defaultPower = model.Pt
    freq = model.freq
    lamb = 3e8/freq
    arq = model.arq

    print("Using parameters from %s radio model." %(model.name))

    return True