from modules import coder
from modules import hadamard

hadamard_matrix = hadamard.hadamard(1)

print(coder.encode("hello", hadamard_matrix[0]))