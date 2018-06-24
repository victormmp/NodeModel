import numpy
import math
from src.NetNode import Link, Node

def calculateLinkPRR(link):
    
    teste1 = Node(0,0)
    teste2 = Node(1,1)
    link1 = Link(teste1, teste2)
    
    SNR = calculateSNR()
    prr = (1 - 0.5 * math.exp())
    
def calculateSNR():
    return P_Tran - PL - Pn
