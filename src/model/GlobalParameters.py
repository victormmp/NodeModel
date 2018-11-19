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
import numpy as np
import sys
from collections import namedtuple
from settings import *
from src.model import LinkService as linkService
from src.model import RadioModels, GeoService
from src.model.NetNode import *

sys.path.insert(0, r'../../')

# MODEL PARAMETERS FOR CALCULATIONS

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
d0 = 3.25                       # Reference distance for Friss formula
defaultRate = 5e6               # Default transmission rate
limiar_snr = 30                 # SNR upper limit in dB
limiar_snr_delta = 1            # SNR lower limit in dB
limiar_prr = 0                  # Lower PRR limit, where communication is impossible

# OPTIMIZATION PARAMETERS

dim = namedtuple("dim",["start", "end"])
area = namedtuple("area", ["top_left", "botom_right"])

N1_DIM = dim(start=(0.0, 0.0), end=(0.0, 10.0))
N2_DIM = dim(start=(0.0, 0.0), end=(10.0, 10.0))
N3_DIM = dim(start=(0.0, 0.0), end=(0.0, 10.0))
N4_DIM = area(top_left=(0.0, 0.0), botom_right=(10.0, 10.0))
SINK_NODE = Node(0.0, 0.0)

# GLOBAL OPTIONS METHODS

def setWhiteNoiseVariance():
   # Pr = linkService.friss(d0)
    Pr = linkService.shadowing(d0)
    global whiteNoiseVariance
    whiteNoiseVariance = Pr/1e4
    

def setTransmissionPowerVariance(variance=None):
    global defaultPower
    global USE_TRANSMISSION_POWER_VARIANCE
    
    if (variance==None):
        # Using a default variance for transmission power of 1%
        variance = 0.01 * defaultPower
    if USE_TRANSMISSION_POWER_VARIANCE:
        defaultPower = defaultPower + np.random.normal(loc=0, scale=variance)
    
    
def initializeGlobalParameters(model):
    getParametersFromModel(model)
    setWhiteNoiseVariance()
    setTransmissionPowerVariance()
    # if LOAD_CONSTANTS_FROM_FILE: loadConstantsFromFile()
    
def set_d0(distance):
    global d0

    d0 = distance

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
        raise TypeError("model is not a valid RadioModel object.")

    global R, Bn, Gt, Gr, defaultPower, freq, lamb, arq

    R = model.R
    Bn = model.Bn
    Gt = model.Gt
    Gr = model.Gr
    defaultPower = model.Pt
    freq = model.freq
    lamb = 3e8/freq
    arq = model.arq

    # print("Using parameters from %s radio model." %(model.name))

    return True


def loadConstantsFromFile(file_path=CONSTANTS_FILE):
    """
    The corresponding file contains the locations of sink node (point (0,0)), the
    coordinates for N1, N2, N3 lines (start and end) and the coordinates for N4 area.
    From the file, all the Points obtained MUST follow the order:

    sink - N1 start - N1 end - N2 start - N2 end - N3 start - N3 end - N4 top left - N4 botom right

    """
    
    global SINK_NODE, N1_DIM, N2_DIM, N3_DIM, N4_DIM

    nodeList = GeoService.getNodesFromGeoJSONFile(file_path)

    SINK_NODE = nodeList.pop(0)

    # nodeCoordinate = [node.getPoints() for node in nodeList]
    nodeCoordinate = [node.getCoordinates() for node in nodeList]

    N1_DIM = dim(start=nodeCoordinate[0], end=nodeCoordinate[1])
    N2_DIM = dim(start=nodeCoordinate[2], end=nodeCoordinate[3])
    N3_DIM = dim(start=nodeCoordinate[4], end=nodeCoordinate[5])
    N4_DIM = area(top_left=nodeCoordinate[6], botom_right=nodeCoordinate[7])

    return SINK_NODE
