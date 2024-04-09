import base64
import socket
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def make_request(socket_r, request_text):
    socket_r.sendall((request_text + '\r\n').encode())


def receive_response(sock):
    response_data = b''
    while True:
        part = sock.recv(65535)
        response_data += part
        if len(part) < 65535:
            break
    return response_data.decode()


def send_email_data(socket_s, message):
    socket_s.sendall(b'DATA' + b'\r\n')
    receive_response(socket_s)

    socket_s.sendall(message.encode('utf-8') + b'\r\n')

    socket_s.sendall(b"\r\n.\r\n")
    return receive_response(socket_s)


class EmailClient:
    def __init__(self, host, port, username, password):
        self.host_addr = host
        self.port = port
        self.user_name = username
        self.password = password

    def send_email(self, from_email, to_email, subject, body, attachments):
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, 'plain'))

        for attachment in attachments:
            msg.attach(attachment)

        full_message = msg.as_string()

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.host_addr, self.port))
                client = ssl.create_default_context().wrap_socket(client, server_hostname=self.host_addr)
                server_response = receive_response(client)
                make_request(client, 'EHLO myUserName')
                base64login = base64.b64encode(self.user_name.encode()).decode()
                base64password = base64.b64encode(self.password.encode()).decode()
                make_request(client, 'AUTH LOGIN')
                make_request(client, base64login)
                make_request(client, base64password)
                make_request(client, 'MAIL FROM: <{}>'.format(from_email))
                make_request(client, "RCPT TO: <{}>".format(to_email))
                final_response = send_email_data(client, full_message)
                print(final_response)
                return True, "Email has been sent successfully!"
        except ssl.SSLError as e:
            print("SSL Error:", e)
            return False, str(e)
        except socket.error as e:
            print("Socket Error:", e)
            return False, str(e)
        except Exception as e:
            print("Other Error:", e)
            return False, str(e)
        finally:
            if client:
                client.close()
