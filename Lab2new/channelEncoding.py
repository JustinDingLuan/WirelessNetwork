import numpy as np
import random
from hammingcode import HammingCode
from crc12code import CRC12Code


def TrasnmitWithNoise(message, noise_rate=0.1):
   occur = False
   for i in range(len(message)):
      if random.random() < noise_rate:
         occur = True
         message[i] ^= 1
   
   return message, occur

def bitstring_to_np(bitstring):    
    return np.array([int(b) for b in bitstring], dtype=int)

def np_to_bitstring(array):    
    return ''.join(str(b) for b in array)

def generateRandomBits(n):
   bits = np.random.randint(0, 2, n)
   return bits

if __name__ == "__main__":
   length = 1024
   data = generateRandomBits(length)     
   Round = length // 8 
   
   for i in range(Round):
      message = data[i*8:(i+1)*8]
      # 我都是用 np array 寫...     
      m = np_to_bitstring(message)
      print("-----------------------------------------")
      print("Round: ", i+1)
      print("Raw message: ", m)
       
      raw_crc_bits = CRC12Code().Encoding(message)
      raw_crc_bits = np.array(list(np.binary_repr(raw_crc_bits, width=12)), dtype=int)
      raw_crc_bits = np_to_bitstring(raw_crc_bits)
      
      encoded_message = HammingCode().Encoding(message)
      encoded_message = encoded_message.astype(int)
      str_encoded_message = np_to_bitstring(encoded_message)
      print("Hamming encoded message: ", str_encoded_message)
      
      print("-----------------------------------------")
      print("Transmitting..., may introduce error")
      encoded_message, noise = TrasnmitWithNoise(encoded_message, 0.05)      
      print("-----------------------------------------")
      
      str_encoded_message = np_to_bitstring(encoded_message)
      print("Received message: ", str_encoded_message)
      
      decoded_message, error, syndrome = HammingCode().Decoding(encoded_message)
      decoded_message = decoded_message.astype(int)
      
      str_decoded_message = np_to_bitstring(decoded_message)
      print("decoded message: ", str_decoded_message)
        
      new_crc_bits = CRC12Code().Encoding(decoded_message)
      new_crc_bits = np.array(list(np.binary_repr(new_crc_bits, width=12)), dtype=int)
      new_crc_bits = np_to_bitstring(new_crc_bits)
      
      if error:
         print("Error position: ", syndrome)      
      print("-----------------------------------------")
      
      print("Raw CRC bits: ", raw_crc_bits)
      print("New CRC bits: ", new_crc_bits)
      
      if np.array_equal(raw_crc_bits, new_crc_bits):
         print("CRC 校驗通過, 解碼成功")
      else:
         print("CRC 校驗失敗, hamming correction 錯誤")
      
      
      
      
   
   
   
   





