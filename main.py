from modules import coder
from modules import hadamard
from modules import BPSK_modulation
from modules import draw_modulation
hadamard_matrix = hadamard.hadamard(2)
enCode1 = coder.encode("hello", hadamard_matrix[0])
enCode2 = coder.encode("kotak", hadamard_matrix[1])
enCode3 = coder.encode("nigga", hadamard_matrix[2])
for i in range(len(enCode1)):
  bpsk1, t1 = BPSK_modulation.bpsk_modulation(enCode1[i], 100)
  bpsk2, t2 = BPSK_modulation.bpsk_modulation(enCode2[i], 100)
  bpsk3, t3 = BPSK_modulation.bpsk_modulation(enCode3[i], 100)
  bpsk = bpsk1 + bpsk2 + bpsk3
  draw_modulation.draw(bpsk)
  demodulated = BPSK_modulation.bpsk_demodulation(bpsk, 100)
  print(coder.decode(demodulated, hadamard_matrix[0]), end = " ")
  print(coder.decode(demodulated, hadamard_matrix[1]), end = " ")
  print(coder.decode(demodulated, hadamard_matrix[2]), end = "\n")