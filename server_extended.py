import socket

SERVER_ADDRESS = ('localhost', 12345)
QUIT_COMMAND = "QUIT"
SHUTDOWN_COMMAND = "SHUTDOWN"
SERVER_SHUTDOWN_MESSAGE = "SERVER_SHUTDOWN"

server_running = True  # Флаг работы сервера

def handle_client(client_socket, client_address):
    global server_running
    print(f"Подключен клиент: {client_address}")
    try:
        while server_running:
            data = client_socket.recv(1024)
            if not data:
                print(f"Клиент {client_address} отключился.")
                break

            message = data.decode('utf-8').strip()

            if not message:
                print(f"Клиент {client_address} отправил пустое сообщение.")
                continue  # Продолжаем ожидать сообщение

            if message == QUIT_COMMAND:
                print(f"Клиент {client_address} запросил отключение.")
                try:
                    client_socket.sendall("BYE".encode('utf-8'))
                except (BrokenPipeError, ConnectionResetError):
                    print(f"Не удалось отправить подтверждение отключения клиенту {client_address}")
                finally:
                    client_socket.close()
                break  # Выход из цикла обработки клиента
            elif message == SHUTDOWN_COMMAND:
                print("Получена команда на выключение сервера.")
                server_running = False
                try:
                    client_socket.sendall(SERVER_SHUTDOWN_MESSAGE.encode('utf-8'))
                except (BrokenPipeError, ConnectionResetError):
                    print(f"Не удалось отправить сообщение об отключении клиенту {client_address}")
                finally:
                    client_socket.close()
                break  # Выход из цикла обработки клиента
            else:
                print(f"Получено сообщение от {client_address}: {message}")
                response = f"Эхо: {message}"
                try:
                    client_socket.sendall(response.encode('utf-8'))
                except (BrokenPipeError, ConnectionResetError):
                    print(f"Не удалось отправить ответ клиенту {client_address}")
                    break # Завершаем работу с клиентом, если не удалось отправить ответ


    except ConnectionResetError:
        print(f"Клиент {client_address} неожиданно разорвал соединение.")
    except Exception as e:
        print(f"Ошибка при обработке клиента {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"Соединение с клиентом {client_address} закрыто.")

def main():
    global server_running

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(1)  # Слушаем только одно подключение
    print(f"Сервер запущен и слушает на {SERVER_ADDRESS}")

    try:
        while server_running:
            client_socket, client_address = server_socket.accept()
            handle_client(client_socket, client_address)
            if not server_running:
                break #  Выходим из цикла accept если сервер должен завершиться

    except KeyboardInterrupt:
        print("Сервер завершает работу по сигналу прерывания.")
    finally:
        server_socket.close()
        print("Сервер остановлен.")

if __name__ == "__main__":
    main()