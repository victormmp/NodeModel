"""
model file for radio solutions. Use this file to change some radio inherit
parameters in global scope with this specific parameters.

    -----------------------------------------------------------------------
    | model Parameters  |                 Description                     |
    |-------------------|-------------------------------------------------|
    | R                 |     Transmission ratio [bps]                    |
    | Bn                |     Noise bandwidth [Hz]                        |
    | Gt                |     Transmission antenna gain [dB]              |
    | Gr                |     Reception antenna gain [dB]                 |
    | Pt                |     Transmission power [W]                      |
    | freq              |     Transmission frequency [Hz]                 |
    | arq               |     Package size [bytes]                        |
    -----------------------------------------------------------------------

"""

class RadioModel:
    R = None        # Transmission ratio [bps]
    Bn = None       # Noise bandwidth [Hz]
    Gt = None       # Transmission antenna gain [dB]
    Gr = None       # Reception antenna gain [dB]
    Pt = None       # Transmission power [W]
    freq = None     # Transmission frequency [Hz]
    arq = None      # Package size [bytes]

    def __init__(self, R, Bn, Gt, Gr, Pt, freq, arq, name = None):
        self.R = R
        self.Bn = Bn
        self.Gt = Gt
        self.Gr = Gr
        self.Pt = Pt
        self.freq = freq
        self.arq = arq
        self.name = name

WirelessHart = RadioModel(
                            name = "WirelessHart",
                            R = None,
                            Bn = None,
                            Gt = None,
                            Gr = None,
                            Pt = None,
                            freq = None,
                            arq = None
                          )

MICA2 = RadioModel(
                    name="MICA2",
                    R = 19e3,
                    Bn = 30e3,
                    Gt = 1,
                    Gr = 1,
                    Pt = 0.2,
                    freq = 2.4e9,
                    arq = 50
                   )

ZigBee = RadioModel(
                        name = "ZigBee",
                        R = 250e3,          # Zigbee comunication rate
                        Bn = 2e6,           # According to 802.15.4 standard
                        Gt = 1.7,
                        Gr = 1.7,
                        Pt = 0.00079,       # -1 dBm, appx 0.8 mW
                        freq = 2.48e9,
                        arq = 60
                   )
