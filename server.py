import socket
import threading

from modules import coder
from modules import hadamard
from modules import BPSK_modulation
from modules import draw_modulation
from modules import interference
import pickle
import numpy as np


def bpsk_modulation_packeges(encoded):
    moduleted = []
    for i in encoded:
        moduleted.append(BPSK_modulation.bpsk_modulation(i, 100))
    return moduleted


def bpsk_demoduleted_packeges(moduleted):
    demoduleted = []
    for i in moduleted:
        demoduleted.append(BPSK_modulation.bpsk_demodulation(i, 100))
    return demoduleted


# Настройки сервера
HOST = "26.81.95.59"  # Локальный хост
PORT = 12345  # Порт, на котором будет работать сервер

hadamard_vectors = hadamard.hadamard(int(np.log2(100) + 1))
used_codes = []
client_size = 0
max_size = 0
clients = {}
client_in_network = {}
all_got_data = []


# Функция для обработки одного клиента
def handle_client(client_socket, client_address):
    global client_size, hadamard_vectors, used_codes, max_size, all_got_data

    print(f"[INFO] Подключен клиент: {client_address}")
    user_data = bytearray()

    try:
        while True:
            # Прием данных от клиента
            # ID = client_socket.recv(1024)
            # response = f"Ваше сообщение будет отправлено клиенту {ID}"
            # client_socket.send(response)  # Даем номер получателю

            data = client_socket.recv(1024)  # Получаем до 1024 байт
            user_data += data
            if not data:
                # Если данных нет, клиент отключился
                print(f"[INFO] Клиент {client_address} отключился")
                all_got_data.extend(pickle.loads(user_data))
                max_size += 1
                break

            # print(f"[RECEIVED] От {client_address}: {data}")

            # Отправляем сообщение дальше
            # response = f"Сервер получил: {data}"
            # client_socket.sendall(response)  # Отправляем ответ
    except Exception as e:
        print(f"[ERROR] Ошибка с клиентом {client_address}: {e}")
    finally:
        client_socket.close()  # Закрываем соединение
        print(f"[INFO] Соединение с {client_address} закрыто")
        client_size -= 1
        if client_size == 0:
            # interfeered = interference.interfere(all_got_data)
            demoduled = bpsk_demoduleted_packeges(all_got_data)
            for i in range(max_size):
                print(coder.packet_decode(demoduled, hadamard_vectors[i]))
            all_got_data = []


# Главная функция сервера
def start_server():
    global hadamard_vectors, client_size

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))  # Привязываем сервер к указанному хосту и порту
    server_socket.listen(128)  # Максимальная очередь подключений — 10

    print(f"[INFO] Сервер запущен на {HOST}:{PORT}")

    try:
        while True:
            # Принимаем входящее соединение
            client_socket, client_address = server_socket.accept()
            print(f"[INFO] Новое соединение от {client_address}")

            data = pickle.dumps(hadamard_vectors[client_size])
            client_socket.sendall(data)

            client_size += 1

            # Запускаем новый поток для обработки клиента
            client_thread = threading.Thread(
                target=handle_client, args=(client_socket, client_address)
            )
            client_thread.start()
    except KeyboardInterrupt:
        print("[INFO] Сервер остановлен вручную")
    finally:
        server_socket.close()
        print("[INFO] Сервер завершил работу")


if __name__ == "__main__":
    start_server()
