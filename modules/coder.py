import numpy as np

def to_binary(i : int) -> list[int]:
  ans = []
  while i > 0:
    ans.append(i % 2)
    i //= 2
  return ans[::-1]

def encode(s: str, hadamard_vector, user_num: int) -> list[int]:
  ans = [[0]]*len(s)
  hadamard_size = int(np.log2(user_num) + 1)
  for i in range(len(s)):
    bits = to_binary(ord(s[i]))
    ans[i] =  [_ * hadamard_vector for _ in bits]
    ans[i] = np.concatenate(ans[i], axis=None)
  return ans

