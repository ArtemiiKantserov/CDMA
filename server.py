import socket
import threading

from modules import coder
from modules import hadamard
from modules import BPSK_modulation
from modules import draw_modulation
from modules import interference
import numpy as np

# Настройки сервера
HOST = "26.81.95.59"  # Локальный хост
PORT = 12345  # Порт, на котором будет работать сервер

hadamard_vectors = hadamard.hadamard(int(np.log2(10) + 1))
client_size = 0
clients = {}
client_in_network ={}

# Функция для обработки одного клиента
def handle_client(client_socket, client_address):
    global client_size

    print(f"[INFO] Подключен клиент: {client_address}")

    try:
        while True:
            # Прием данных от клиента
            ID = client_socket.recv(1024)
            response = f"Ваше сообщение будет отправлено клиенту {ID.decode("utf-8")}"
            client_socket.send(response.encode("utf-8"))  # Просим номер получателя
            
            data = client_socket.recv(1024)  # Получаем до 1024 байт
            if not data:
                # Если данных нет, клиент отключился
                print(f"[INFO] Клиент {client_address} отключился")
                break

            print(f"[RECEIVED] От {client_address}: {data.decode('utf-8')}")

            # Отправляем сообщение дальше
            response = f"Сервер получил: {data.decode('utf-8')}"
            client_socket.send(response.encode("utf-8"))  # Отправляем ответ
    except Exception as e:
        print(f"[ERROR] Ошибка с клиентом {client_address}: {e}")
    finally:
        client_socket.close()  # Закрываем соединение
        print(f"[INFO] Соединение с {client_address} закрыто")
        client_size -= 1


# Главная функция сервера
def start_server():
    global hadamard_vectors, client_size

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))  # Привязываем сервер к указанному хосту и порту
    server_socket.listen(10)  # Максимальная очередь подключений — 10

    print(f"[INFO] Сервер запущен на {HOST}:{PORT}")

    try:
        while True:
            # Принимаем входящее соединение
            client_socket, client_address = server_socket.accept()
            print(f"[INFO] Новое соединение от {client_address}")

            clients[client_size] = client_socket
            client_size += 1

            responce = f"{hadamard_vectors[client_size - 1]}"
            client_socket.send(responce.encode("utf-8"))

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
