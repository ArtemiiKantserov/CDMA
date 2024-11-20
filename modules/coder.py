import numpy as np

def to_binary(i : int) -> np.array:
  ans = [-1]*8
  j = 0
  while i > 0:
    ans[j] = (1 if i % 2 > 0 else -1)
    j += 1
    i //= 2
  return ans[::-1]

def binary_to_char(bits: np.array):
  ans = 0
  bits = bits[::-1]
  for i in range(len(bits)):
    ans += bits[i] * 2**i
  return chr(ans)

def encode(s: str, hadamard_vector: np.array) -> np.ndarray:
  ans = [[0]*len(hadamard_vector)]*len(s)
  # print(ans)
  for i in range(len(s)):
    bits = to_binary(ord(s[i]))
    # print(2 * bits[0] * hadamard_vector)
    ans[i] =  [_ * hadamard_vector for _ in bits]
    ans[i] = np.concatenate(ans[i], axis=None)
  return ans

def decode(code: np.ndarray, hadamard_vector: np.array) -> str:
  matrix = [code[i:i+len(hadamard_vector)] for i in range(0, len(code), len(hadamard_vector))]
  multiplied = np.matmul(matrix, hadamard_vector)
  ans = [1 if i > 0 else 0 for i in multiplied]
  return binary_to_char(ans)
  