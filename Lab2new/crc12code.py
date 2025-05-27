import numpy as np
import math


class CRC12Code:
   def __init__(self):
      pass   
   
   def Encoding(self, message):
      # 12 bits CRC x^12 + x^11 + x^3 + x^2 + x + 1
      # 0x80F = 1000 0000 1111    
      width = 12
      poly = 0x180F 
      crc = 0 
      
      for bit in message:
        # 將 crc 左移一位並加入當前 bit
        crc = (crc << 1) | int(bit)
        # 當 crc 超出 12 位（即第 13 個 bit 為 1）時，執行 XOR
        if crc & (1 << width):
            crc ^= poly

      # 資料讀取完後，附加 12 個 0 進行「沖洗」運算
      for i in range(width):
         crc <<= 1
         if crc & (1 << width):
               crc ^= poly

      # 取 crc 的低 12 位作為結果
      return crc & ((1 << width) - 1)

   def Decoding(self, received_message):
      # 12 bits CRC x^12 + x^11 + x^3 + x^2 + x + 1
      # 0x80F = 1000 0000 1111
      width = 12
      poly = 0x180F
      crc = 0
      error = False
      
      for bit in received_message:
         crc = (crc << 1) | int(bit)
         if crc & (1 << width):
            crc ^= poly
      
      if crc != 0:
         error = True
      decoded_message = np.array(received_message[:-width])
      return decoded_message, error
