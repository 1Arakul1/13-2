import socket
import sys

SERVER_ADDRESS = ('localhost', 12345)
SHUTDOWN_COMMAND = "SHUTDOWN"
QUIT_COMMAND = "QUIT"

def main():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(SERVER_ADDRESS)
        server_running = True  # Флаг, что сервер, предположительно, работает

        while server_running:
            message = input("Введите сообщение (или QUIT для выхода, SHUTDOWN для выключения сервера): ")

            if message == QUIT_COMMAND:
                try:
                    client_socket.sendall(message.encode('utf-8'))
                    response = client_socket.recv(1024).decode('utf-8')
                    if response == "BYE":
                        print("Отключение от сервера.")
                        break
                except (ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError):
                    print("Сервер разорвал соединение.")
                    break

            elif message == SHUTDOWN_COMMAND:
                try:
                    client_socket.sendall(message.encode('utf-8'))
                    response = client_socket.recv(1024).decode('utf-8')
                    if response == "SERVER_SHUTDOWN":
                        print("Сервер завершает работу.")
                        server_running = False #  Больше не пытаемся отправлять сообщения
                        break  # Выходим из цикла, не отправляя QUIT
                except (ConnectionRefusedError, ConnectionAbortedError, ConnectionResetError):
                    print("Разрыв подключения")
                    break

            elif message:
                try:
                    client_socket.sendall(message.encode('utf-8'))
                    response = client_socket.recv(1024).decode('utf-8')
                    print(f"Ответ сервера: {response}")
                except (ConnectionResetError, ConnectionAbortedError):
                    print("Разрыв подключения")
                    break

            else:
                print("Пожалуйста, введите сообщение.")


    except ConnectionRefusedError:
        print("Не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        client_socket.close()
        print("Process finished with exit code 0")

if __name__ == "__main__":
    main()