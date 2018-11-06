import os
import numpy as np
import sys
import src.model.LinkService as LinkService
from src.model.NetNode import Node, Link
from src.model.RadioModels import ZigBee
import src.model.GlobalParameters as gp
from sklearn import metrics
import scipy.optimize as scpy
import src.utils.OptimizationAlgorithms as opt

sys.path.insert(0, r'../')
files = os.listdir(r'./')

#%% POSITIONS COORDINATES

POSITIONS = [[-19.873300, -43.963470],
             [-19.873620, -43.963860],
             [-19.873770, -43.964440],
             [-19.874100, -43.964980],
             [-19.874380, -43.965420]
            ]

NOISE_FLOOR= -85 # Need the correct measurement of the noise floor

#%% FILE PARSE

# Filter txt files
files = [file for file in files if file.endswith('.txt')]

rssi_list = []

# Get RSSI for each file list
for file in files:
    
    
    # Read file data
    with open(file) as f:
        lines = f.readlines()
        lines = lines[3:]
    
    # Parse data in each line and get rssi
    rssi_list.append(np.mean([float(line.split(',')[3]) for line in lines]))

# Get the SNR for corresponding RSSI

snr_measurements = [rssi - NOISE_FLOOR for rssi in rssi_list]


#%% CREATE NODES AND LINKS
    
nodes = []
for coordinate in POSITIONS:
    node = Node()
    node.extractNode(coordinate, POSITIONS[0])
    nodes.append(node)

links = [Link(node, nodes[0]) for node in nodes[1:]]

#%% GET SNR FOR EACH LINK

gp.initializeGlobalParameters(ZigBee)

def error_func(d):
    gp.set_d0(d)
    gp.initializeGlobalParameters(ZigBee)
    snr_list = [LinkService.getSNR(LinkService.shadowing(link.distance)) for link in links]
    err = metrics.mean_absolute_error(snr_measurements, snr_list)
    return err

#%% OPTIMIZE D0
MAX_ITERATION = 100

iteration = 0
result_list = []
while iteration < MAX_ITERATION:
    iteration += 1
    result_list.append(opt.golden_ratio(error_func))
    
result = np.mean(result_list)
print(result)
    
    