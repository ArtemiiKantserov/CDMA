from modules import coder
from modules import hadamard
from modules import BPSK_modulation

hadamard_matrix = hadamard.hadamard(1)
enCode = coder.encode("helloniggaasd", hadamard_matrix[0])
enCode1 = coder.encode("world", hadamard_matrix[1])
got1, got2 = "", ""

for i in range(min(len(enCode), len(enCode1))):
  bpsk, t = BPSK_modulation.bpsk_modulation(enCode[i], 100, 1000)
  demodulated = BPSK_modulation.bpsk_demodulation(bpsk, 100, 1000)
  bpsk1, t1 = BPSK_modulation.bpsk_modulation(enCode1[i], 100, 1000)
  demodulated1 = BPSK_modulation.bpsk_demodulation(bpsk1, 100, 1000)
  got1 += coder.decode(demodulated, hadamard_matrix[0])
  got2 += coder.decode(demodulated1, hadamard_matrix[1])
  
for i in range(min(len(enCode), len(enCode1)), max(len(enCode), len(enCode1))):
  bpsk, t = BPSK_modulation.bpsk_modulation(enCode[i], 100, 1000)
  demodulated = BPSK_modulation.bpsk_demodulation(bpsk, 100, 1000)
  got1 += coder.decode(demodulated, hadamard_matrix[0])
  
print(got1)
print(got2)