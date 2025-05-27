import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.stats import binom

def csma_generalized(arrival_times: np.ndarray, p, cd: bool = False, alpha: float = 0.01) -> int:
    success = 0
    transmission_ends = 0
    collision_detect_possible = 0
    successfully_sending = False
    pending_packets = 0
    
    for j, time in enumerate(arrival_times):
        if time < collision_detect_possible:
            # channel is busy, but detected as free due to alpha delay in detection of ongoing transmission
            if cd:
                transmission_ends = min(transmission_ends, time + alpha)
            else:
                transmission_ends = time + 1
            if successfully_sending:
                success -= 1
                successfully_sending = False
        elif time < transmission_ends:
            # channel is busy, do nothing
            pending_packets += 1
            if (j + 1 < len(arrival_times) and arrival_times[j + 1] >= transmission_ends) \
                    or j + 1 == len(arrival_times):
                if p == 1:
                    x = pending_packets
                elif p == 0:
                    x = 0
                else:
                    x = binom(pending_packets, p).rvs()
                if x == 1:
                    success += 1
                    successfully_sending = True
                    collision_detect_possible = transmission_ends + alpha
                    transmission_ends = transmission_ends + 1
                elif x > 1:
                    collision_detect_possible = transmission_ends + alpha
                    transmission_ends = transmission_ends + 1
                pending_packets = 0
        else:
            # channel is free
            successfully_sending = True
            success += 1
            collision_detect_possible = time + alpha
            transmission_ends = time + 1
    return success

N = int(1e4)
numG = 500
rng = np.random.default_rng()
throughput_pt01persistent = np.zeros(numG)
throughput_pt1persistent = np.zeros(numG)
throughput_pt5persistent = np.zeros(numG)
# 10^(-1.5) ~ 10^(1)，共 numG 個點，間隔是 log scale
G = np.logspace(-1.5, 1, numG)

if __name__ == "__main__":
    for i, lam in enumerate(G):
        inter_arrival_time = rng.exponential(1 / lam, N)
        arrival_times = np.array(inter_arrival_time)
        
        for j in range(1, len(arrival_times)):
            arrival_times[j] += arrival_times[j - 1]
    
        throughput_pt1persistent[i] = csma_generalized(arrival_times, 0.1) / math.ceil(arrival_times[-1])
        throughput_pt01persistent[i] = csma_generalized(arrival_times, 0.01) / math.ceil(arrival_times[-1])
        throughput_pt5persistent[i] = csma_generalized(arrival_times, 0.5) / math.ceil(arrival_times[-1])
    
    
    plt.figure(figsize=(8, 6))
    plt.plot(G, throughput_pt1persistent, label="CSMA 0.1-persistent")
    plt.plot(G, throughput_pt5persistent, label="CSMA 0.5-persistent")
    plt.plot(G, throughput_pt01persistent, label="CSMA 0.01-persistent")    
    plt.xlabel('G (attempts rate)', fontsize=14)
    plt.ylabel('S (throughput per frame time)', fontsize=14)
    plt.title('CSMA Throughput vs Traffic Load', fontsize=16)
    plt.legend() 
    plt.grid(True)   
    plt.show()
    
    