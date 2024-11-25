import socket

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
    print(f"[ОТВЕТ СЕРВЕРА] {response.decode('utf-8')}")

    while True:
        # Отправка сообщения
        message = input("Введите сообщение (или 'exit' для выхода): ")
        if message.lower() == 'exit':
            break
        client_socket.send(message.encode('utf-8'))

        # Прием ответа от сервера
        response = client_socket.recv(1024)
        print(f"[ОТВЕТ СЕРВЕРА] {response.decode('utf-8')}")
