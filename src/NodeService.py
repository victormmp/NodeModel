import math
import numpy
from src.NetNode import Link, Node
from src.GlobalParameters import GlobalParameters

gp = GlobalParameters()

def calculateLinkPRR(link):
    
    teste1 = Node(0,0)
    teste2 = Node(1,1)
    link1 = Link(teste1, teste2)
    SNR = calculateSNR()
    prr = (1-0.5*(math.exp(-(SNR/2)*(1/(gp.R/gp.Bn)))))^(8*Arq)

    return prr

def calculateSNR():
    return P_Tran - PL - Pn
