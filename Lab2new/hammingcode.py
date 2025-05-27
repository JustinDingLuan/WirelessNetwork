import numpy as np
import math

class HammingCode:
   def __init__(self):
      pass
         
   # 由左到右看 array，但正常在處理 array 是由右到左
   def Encoding(self, message):       
      m_bits = len(message)
      hamming_bits = 0
      
      # 計算有幾個 hamming bits
      while 2**hamming_bits - 1 < m_bits + hamming_bits:
         hamming_bits += 1
      total_bits = m_bits + hamming_bits   
      encoded_data = np.zeros(total_bits)
      
      # 放 data bits
      # # 如果是 2 的次方 => hamming bits => 跳過
      index = m_bits - 1
      for i in range(total_bits - 1, -1, -1):      
         # 2的次方 => 0100, 2的次方-1 => 0011 => bitwise and = 全0
         if (total_bits - i & (total_bits - i - 1)) == 0:
            continue
         encoded_data[i] = message[index]
         index -= 1
      
      # 計算 hamming bits
      hamming_code = 0   
      for i in range(total_bits - 1, -1, -1):
         if encoded_data[i] == 1:         
            hamming_code ^= (total_bits - i)
      
      # 放 hamming bits      
      parity_bit_index = 0
      p = 1
      while p <= total_bits:
         parity_value = (hamming_code >> parity_bit_index) & 1
         encoded_data[total_bits - p] = parity_value
         parity_bit_index += 1
         p *= 2 
            
      return encoded_data
   
   def Decoding(self, encoded_data):
      total_bits = len(encoded_data)
      correction_bits = math.floor(math.log2(total_bits)) + 1      
      syndrome = 0
      error = False
      corrected_data = np.zeros(total_bits - correction_bits)      
      
      for i in range(total_bits - 1, -1, -1):         
         if encoded_data[i] == 1:            
            syndrome ^= (total_bits - i)            
      
      if syndrome != 0:
         error = True         
         encoded_data[total_bits - syndrome] ^= 1       
         
      index = total_bits - correction_bits - 1      
      for i in range(total_bits - 1, -1, -1):
         if ((total_bits - i) & (total_bits - i - 1)) != 0:            
            corrected_data[index] = encoded_data[i]
            index -= 1
            
      return corrected_data, error, syndrome  