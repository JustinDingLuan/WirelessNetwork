import numpy as np
import matplotlib.pyplot as plt
import p_persistent_CSMA as P_CSMA
import math

# Define the range of offered load G
numG = 100
G = np.linspace(1e-5, 10, numG)

# Normalized propagation delay (τ/T)
alpha = 0.01

# ALOHA
throughput_pure_ALOHA = G * np.exp(-2 * G)  # Pure ALOHA
throughput_slotted_ALOHA = G * np.exp(-G)   # Slotted ALOHA

# CSMA 
# Non-persistent CSMA
# slotted
throughput_non_persistent = alpha * (G * np.exp(-alpha * G)) / (1 - np.exp(-alpha * G) + alpha)

# 1-persistent CSMA 
numer_1 = G * np.exp(-G * (1 + 2 * alpha)) * (1 + G + G * alpha * (1 + G + 0.5 * G * alpha))
denom_1 = G * (1 + 2 * alpha) - (1 - np.exp(-G * alpha)) + (1 + G * alpha) * np.exp(-G * (1 + alpha))
throughput_1persistent = numer_1 / denom_1

# P-Persistent CSMA 
N = int(1e4)

rng = np.random.default_rng()
throughput_01persistent = np.zeros(numG)
throughput_05persistent = np.zeros(numG)
throughput_001persistent = np.zeros(numG)

for i, lam in enumerate(G):
   # 隨機生成每兩封包的間隔時間
   inter_arrival_time = rng.exponential(1 / lam, N)   
   arrival_times = np.array(inter_arrival_time)
   # 把每個封包的到達時間轉換成總累積時間 -> 表示每個封包在 T = ? 的時間到達   
   # for j in range(1, len(arrival_times)):
   #    arrival_times[j] += arrival_times[j - 1]
   arrival_times = np.cumsum(arrival_times)
    
   throughput_01persistent[i] = P_CSMA.csma_generalized(arrival_times, 0.1, alpha) / math.ceil(arrival_times[-1])
   throughput_05persistent[i] = P_CSMA.csma_generalized(arrival_times, 0.5, alpha) / math.ceil(arrival_times[-1])
   throughput_001persistent[i] = P_CSMA.csma_generalized(arrival_times, 0.01, alpha) / math.ceil(arrival_times[-1])



# Plotting
plt.figure(figsize=(8, 6))
plt.plot(G, throughput_pure_ALOHA,        label='Pure ALOHA')
plt.plot(G, throughput_slotted_ALOHA,     label='Slotted ALOHA')
plt.plot(G, throughput_non_persistent,    label='Non-persistent CSMA')
plt.plot(G, throughput_1persistent,       label='1-persistent CSMA')
plt.plot(G, throughput_01persistent,      label='0.1-persistent CSMA')
plt.plot(G, throughput_05persistent,      label='0.5-persistent CSMA')
plt.plot(G, throughput_001persistent,     label='0.01-persistent CSMA')

plt.xlabel('Traffic Load G', fontsize=14)
plt.ylabel('S: Throughput', fontsize=14)
plt.title('Throughput vs Traffic Load', fontsize=16)
plt.legend()
plt.grid(True)
plt.show()
