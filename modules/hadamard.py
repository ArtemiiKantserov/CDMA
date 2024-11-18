import numpy as np

def hadamard(n: int):
  if n == 0:
    return np.array([[1]])
  else:
    H = hadamard(n - 1)
    return np.block([[H, H], [H, -H]])
