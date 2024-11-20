from modules import coder
from modules import hadamard
from modules import BPSK_modulation
from modules import draw_modulation
from modules import interference
import numpy as np

users_num = int(input("Enter number of users: "))
hadamard_matrix = hadamard.hadamard(int(np.log2(users_num)+1))
strings = []
min_len = 1e20

for i in range(users_num):
  strings.append(input())
  min_len = min(min_len, len(strings[i]))

strings.sort(key = len, reverse=True)
print(strings)

while strings != []:
  bpsk_s, delete_strs = [[]]*min_len, []
  encoded = [np.concatenate([coder.encode(strings[t][i], hadamard_matrix[t]) for i in range(min_len)]) for t in range(len(strings))] 
  
  for t in range(len(strings)):
    if(len(strings[t]) == min_len):
      delete_strs.append(t)
      
  for i in range(min_len):
    for j in range(len(strings)):
      print(encoded[j][i])
      bpsk_i, _ = BPSK_modulation.bpsk_modulation(encoded[j][i], 100)
      bpsk_s[i].append(bpsk_i)
      
    bpsk = interference.interfere(bpsk_s[i])
    draw_modulation.draw(bpsk)
    demodulated = BPSK_modulation.bpsk_demodulation(bpsk, 100)
    print(demodulated)
    for j in range(len(strings)):
      print(coder.decode(demodulated, hadamard_matrix[j]), end = " ")
    print("")
  
  for t in delete_strs[::-1]:
    strings.pop(t)
    
  for i in range(len(strings)):
    strings[i] = strings[i][min_len:]
    
  if strings!=[]:
    min_len = len(min(strings, key = len))
  
  print(strings)
