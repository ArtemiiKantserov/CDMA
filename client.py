import socket
import threading
from modules import coder
from modules import BPSK_modulation

def create_hadamard(s : str):
    s = s.strip('[]')
    vec = [int(i) for i in s.split()]
    n = len(vec) // 4
    hadamard = []
    for i in range(0, n * 4, n):
        hadamard.append([vec[i:i+n]])
        return hadamard
def mess_server(client_socket, size = 1024):
    while True:
        response = client_socket.recv(size)
        print(f"{response.decode('utf-8')}")

# Настройки клиента
HOST = '26.81.95.59'  # IP сервера
PORT = 12345        # Порт сервера
inp = input("Введите IP и порт для подключения в виде n.n.n.n port: ").split()
HOST = inp[0]
PORT = int(inp[1])
# Подключение к серверу
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    print("[INFO] Подключен к серверу")
    response = client_socket.recv(1024)
    s = response.decode('utf-8')
    hadamard = create_hadamard(s)
    input_sever = threading.Thread(
        target=mess_server, args=(client_socket, 1024)
    )
    input_sever.start()
    response.decode('utf-8')
    while True:
        # Отправка сообщения
        message = input("Введите сообщение (или 'exit' для выхода): ")
        if message.lower() == 'exit':
            break
        strings = []
        for j in range(len(message) // 1024 + 1):
            strings.append(message[1024*j:1024*(j+1)])
        print(strings)
        strings[-1] += '/0' * (1024 - len(strings[-1]))
        encoded = [coder.packet_encode(i, hadamard) for i in strings]
        bpsk_s = []
        print(encoded[0][0])
        for i in encoded:
            for j in i:
                bpsk_i, _ = BPSK_modulation.bpsk_modulation(j, 100)
                bpsk_s.append(bpsk_i)
        demodulated = BPSK_modulation.bpsk_demodulation(bpsk_s, 100)
        decoded = coder.packet_decode(demodulated, hadamard)
        #хотели разбить на потоки, чтобы каждый пакет по 1024 байта преобразовывался и отправлялся независимо(для ускорения процесса), но проблемы с увеличением веса пакета из-за bpsk
        # for i in bpsk_s:
            # client_socket.sendall(i.encode('utf-8'))
        # Прием ответа от сервера
        # response = client_socket.recv(1024)
        # print(f"[ПОЛУЧЕНО СООБЩЕНИЕ] {response.decode('utf-8')}")
