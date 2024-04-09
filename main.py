import tkinter as tk
from tkinter import filedialog, messagebox, Label, Entry, Text, Button
from tkinter.simpledialog import Dialog
from email import encoders
from email.mime.base import MIMEBase
from os.path import basename

from email_client import EmailClient


def select_file():
    filetypes = (('Image files', '*.png;*.jpg;*.jpeg;*.gif'),
                 ('All files', '*.*'))
    filename = filedialog.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
    return filename


class SettingsDialog(Dialog):
    def __init__(self, parent, title=None, initial_data=None):
        self.initial_data = initial_data
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text='SMTP Host:').grid(row=0)
        tk.Label(master, text='SMTP Port:').grid(row=1)
        tk.Label(master, text='Username:').grid(row=2)
        tk.Label(master, text='Password:').grid(row=3)

        self.host_entry = tk.Entry(master)
        self.port_entry = tk.Entry(master)
        self.username_entry = tk.Entry(master)
        self.password_entry = tk.Entry(master, show='*')

        if self.initial_data:
            self.host_entry.insert(0, self.initial_data.get('host', ''))
            self.port_entry.insert(0, self.initial_data.get('port', ''))
            self.username_entry.insert(0, self.initial_data.get('username', ''))
            self.password_entry.insert(0, self.initial_data.get('password', ''))

        self.host_entry.grid(row=0, column=1)
        self.port_entry.grid(row=1, column=1)
        self.username_entry.grid(row=2, column=1)
        self.password_entry.grid(row=3, column=1)

        return self.host_entry

    def buttonbox(self):
        box = tk.Frame(self)

        ok_button = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        ok_button.pack(side=tk.LEFT, padx=5, pady=5)
        cancel_button = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def validate(self):
        try:
            port = int(self.port_entry.get())
            if port < 0 or port > 65535:
                raise ValueError("Invalid port number")
            return True
        except ValueError:
            tk.messagebox.showwarning(
                "Invalid Value",
                "Please enter a valid port number (0-65535).",
                parent=self
            )
            return False

    def apply(self):
        self.result = {
            'host': self.host_entry.get(),
            'port': int(self.port_entry.get()),
            'username': self.username_entry.get(),
            'password': self.password_entry.get()
        }


class Application:
    def __init__(self, root):
        self.root = root
        self.root.title('SMTP Client')

        Label(root, text="From:").grid(row=0, column=0, sticky='w')
        self.from_entry = Entry(root, width=50)
        self.from_entry.grid(row=0, column=1, columnspan=2)

        Label(root, text="To:").grid(row=1, column=0, sticky='w')
        self.to_entry = Entry(root, width=50)
        self.to_entry.grid(row=1, column=1, columnspan=2)

        Label(root, text="Subject:").grid(row=2, column=0, sticky='w')
        self.subject_entry = Entry(root, width=50)
        self.subject_entry.grid(row=2, column=1, columnspan=2)

        Label(root, text="Body:").grid(row=3, column=0, sticky='nw')
        self.body_text = Text(root, width=50, height=10)
        self.body_text.grid(row=3, column=1, columnspan=2)

        self.attachments = []
        self.attach_button = Button(root, text="Attach", command=self.attach_file)
        self.attach_button.grid(row=4, column=0, sticky='w')

        self.send_button = Button(root, text="Send", command=self.send_email)
        self.send_button.grid(row=4, column=2, sticky='e')

        self.settings_button = Button(root, text="Settings", command=self.open_settings_dialog)
        self.settings_button.grid(row=5, column=2, sticky='w')

        self.email_client = None

    def attach_file(self):
        filename = select_file()
        if filename:
            with open(filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={basename(filename)}",
            )
            self.attachments.append(part)

    def open_settings_dialog(self, initial_settings=None):
        #  initial_settings = {
        #     'host': 'smtp.yandex.ru',
        #     'port': 465,
        #     'username': '',
        #     'password': '',
        # }
        dlg = SettingsDialog(self.root, "SMTP Settings", initial_data=initial_settings)
        if dlg.result:  # Проверяем, что результат не None.
            self.email_client = EmailClient(**dlg.result)
            print(dlg.result)

    def send_email(self):
        if self.email_client:
            from_email = self.from_entry.get()
            to_email = self.to_entry.get()
            subject = self.subject_entry.get()
            body = self.body_text.get("1.0", tk.END)

            success, message = self.email_client.send_email(from_email, to_email, subject, body, self.attachments)

            if success:
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)
        else:
            messagebox.showwarning("Warning", "Please set up email settings first.")


def main():
    root = tk.Tk()
    app = Application(root)
    root.mainloop()


if __name__ == '__main__':
    main()
