"""
Global parameter class object. Specified class to store all model parametes,
such as transmission power and noise floor.
MUST be called in every project file.

"""


class GlobalParameters:

    R = None
    Bn = None
    whiteNoiseVariance = None
    defaultPower = 0.2              # Transmission power
    Pr = None                       # Received power available
    Gt = 1                          # Effective transmitter antenna area
    Gr = 1                          # Effective receiver antenna area
    freq = 2.4e9                    # Transmission frequency
    lamb = 3e8/freq                 # Wavelength of the transmitted signal
    L = 1                           # Distance between transmitter and receiver
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
        self.getPr()
        self.setWhiteNoiseVariance()

    def getPr(self):
        """
        Pr is the power available at the receiver antenna
        :return:
        """
        pass

    def friis(self):
        pass

    def setWhiteNoiseVariance(self):
        self.whiteNoiseVariance = self.Pr/1e4
