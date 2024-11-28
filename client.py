import socket
import threading
from modules import coder
from modules import BPSK_modulation
from modules import draw_modulation
import pickle

precalculated_hadamard = []
def create_hadamard(s: str):
    s = s.strip("[]")
    vec = [int(i) for i in s.split()]
    return vec


def precalculation(hadamard):
    for i in range(128):
        temp = []
        for j in coder.bits[i]:
            temp.extend([j * h for h in hadamard])
        precalculated_hadamard.append(temp)
    return precalculated_hadamard

def encode_packages(s : str):
    encoded = []
    for i in range(len(s)):
        encoded.append([])
        for j in s[i]:
            encoded[i].append(precalculated_hadamard[ord(j)])
    return encoded

def get_key(d, value):
    for i in range(len(d)):
        fl = True
        for j in range(len(d[i])):
            if d[i][j] != value[j]:
                fl = False
                break
        if fl:
            return i
    raise RuntimeError()

def decode_packages(encoded):
    decoded = ""
    # print(len(precalculated_hadamard[0]))
    for j in encoded:
        for i in range(0, len(j), len(precalculated_hadamard[0])):
            try:
                decoded += chr(get_key(precalculated_hadamard, j[i:i+len(precalculated_hadamard[0])]))
            except RuntimeError:
                continue
    return decoded

def decode_packages_sigma(encoded, hadamard):
    ans = ""
    for i in encoded:
        # print(i)
        for j in range(0, len(i), len(precalculated_hadamard[0])):
            ans += coder.decode(i[j:j + len(precalculated_hadamard[0])], hadamard)
    return ans

def bpsk_modulation_packeges(encoded):
    moduleted = []
    for i in encoded:
        for j in i:
            moduleted.append(BPSK_modulation.bpsk_modulation(j, 100))
    return moduleted

def bpsk_demoduleted_packeges(moduleted):
    demoduleted = []
    for i in moduleted:
        demoduleted.append(BPSK_modulation.bpsk_demodulation(i, 100))
    return demoduleted


# def mess_server(client_socket, size=1024):
#     while True:
#         response = client_socket.recv(size)
#         print(f"{response.decode('utf-8')}")

# Настройки клиента
HOST = "26.81.95.59"  # IP сервера
PORT = 12345  # Порт сервера
inp = input("Введите IP и порт для подключения в виде n.n.n.n port: ").split()
HOST = inp[0]
PORT = int(inp[1])
# Подключение к серверу
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    print("[INFO] Подключен к серверу")
    response = client_socket.recv(4096)
    hadamard = pickle.loads(response)
    precalculated_bits = precalculation(hadamard)
    # input_sever = threading.Thread(target=mess_server, args=(client_socket, 1024))
    # input_sever.start()
    while True:
        # Отправка сообщения
        message = input("Введите сообщение (или 'exit' для выхода): ")
        if message.lower() == "exit":
            break
        strings = []
        for j in range(len(message) // 1024 + 1):
            strings.append(message[1024 * j : 1024 * (j + 1)])
        # print(strings)
        # strings[-1] += "\0" * (1024 - len(strings[-1]))
        encoded = encode_packages(strings)
        moduleted = bpsk_modulation_packeges(encoded)
        # de = bpsk_demoduleted_packeges(moduleted)
        # print(len(moduleted), len(moduleted[0]))
        # print(de[0])
        # print(de)
        # print(decode_packages_sigma(de, hadamard))
        data = pickle.dumps(moduleted)
        client_socket.sendall(data)
