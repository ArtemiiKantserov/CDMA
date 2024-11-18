from modules import coder
from modules import hadamard
from modules import BPSK_modulation
from modules import draw_modulation
hadamard_matrix = hadamard.hadamard(1)
enCode = coder.encode("hello", hadamard_matrix[0], 1)
bpsk, t = BPSK_modulation.bpsk_modulation(enCode[0], 100, 2000)
print(enCode[0])
print(BPSK_modulation.bpsk_demodulation(bpsk, 100, 2000))
draw_modulation.draw(bpsk, 1000)