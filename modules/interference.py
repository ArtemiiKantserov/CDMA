import numpy as np
def interfere(array_of_bits):
  ans = array_of_bits[0]
  for i in range(1, len(array_of_bits)):
    ans += array_of_bits[i]
  return ans
