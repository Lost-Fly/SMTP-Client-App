# PyMailClient
A Python-based SMTP email client that enables users to send emails with attachments through a GUI built with Tkinter. The client leverages sockets and SSL/TLS for secure communication with mail servers.

## Description

PyMailClient is a simple, yet secure, Python-based SMTP client that provides users with the ability to send emails with attachments via a graphical user interface (GUI). The application employs sockets and SSL/TLS encryption to ensure that communication with the email server is secure. PyMailClient features a settings dialog where users can configure SMTP server details, and the core email functionality is wrapped in a user-friendly Tkinter GUI.

## Technologies and Libraries Used

- **Python**: The core programming language used for the project.
- **sockets**: A low-level networking interface to send and receive data over the network.
- **ssl**: A module to provide access to Transport Layer Security (often known as “Secure Sockets Layer”) encryption and peer authentication facilities for network sockets.
- **email.mime**: Modules to create and manipulate email messages, including attachments.
- **Tkinter**: The standard GUI toolkit for Python used to create the interface.
- **base64**: A module to encode binary data to ASCII characters and vice versa, often used when dealing with authentication mechanisms.

## Features and Capabilities

- Send emails with a subject and body text.
- Attach multiple files to an email before sending.
- Configure SMTP host details like host address, port, username, and password.
- Use SSL/TLS for secure communication with the mail server.
- GUI provides an easy-to-use interface for all operations.

## How to Use

To use PyMailClient, follow these steps:

1. Run the application to open the main GUI window.
2. Click on the `Settings` button to open the SMTP settings dialog.
3. Enter details such as the SMTP host, port, username, and password, and then click OK.
4. In the main window, fill in the `From`, `To`, `Subject`, and `Body` fields.
5. If you want to attach files, click on the `Attach` button and select the files you wish to include.
6. Once you're ready, click the `Send` button to send the email.

Ensure that the SMTP settings match those required by your email service provider. Some email services require app-specific passwords or changes in account settings to allow access by third-party clients.

## App GUI:

![image](https://github.com/Lost-Fly/SMTP-Client-App/assets/114507453/00e04341-06bc-4cef-b169-50fd55232d34)
![image](https://github.com/Lost-Fly/SMTP-Client-App/assets/114507453/0f9723fc-646d-481c-900b-ca3611d2b106)
