import tkinter as tk
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import clipboard

from Crypto.Util.Padding import pad, unpad
import base64

class AESCipher:
    def __init__(self, key):
        self.key = key.encode('utf-8')
        self.bs = 16

    def encrypt(self, plaintext):
        plaintext = plaintext.encode('utf-8')
        cipher = AES.new(self.key, AES.MODE_CBC)
        padded_plaintext = pad(plaintext, self.bs)
        ciphertext = cipher.encrypt(padded_plaintext)
        iv = base64.b64encode(cipher.iv).decode('utf-8')
        encrypted_text = base64.b64encode(ciphertext).decode('utf-8')
        return iv + encrypted_text

    def decrypt(self, ciphertext):
        iv = base64.b64decode(ciphertext[:24])
        ciphertext = base64.b64decode(ciphertext[24:])
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        plaintext = cipher.decrypt(ciphertext)
        unpadded_plaintext = unpad(plaintext, self.bs)
        return unpadded_plaintext.decode('utf-8')

class Encrypt_Decrypt(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):

        # tạo frame chứa nội dung
        self.content = tk.Frame(self.master, bg="#fff")
        self.content.pack(side="right", fill="both", expand=True)

        # tạo nội dung cho phần Encrypt
        self.encrypt_content = tk.Frame(self.content, bg="#fff")
        self.encrypt_label = tk.Label(
            self.encrypt_content, text="Nhập text và key:", font=("Helvetica", 14))
        self.encrypt_label.grid(
            row=0, column=0, columnspan=2, padx=10, pady=10)

        self.encrypt_text_label = tk.Label(
            self.encrypt_content, text="Text:", font=("Helvetica", 12))
        self.encrypt_text_label.grid(row=1, column=0, padx=10, pady=5)

        self.encrypt_text_entry = tk.Entry(
            self.encrypt_content, width=40, font=("Helvetica", 12))
        self.encrypt_text_entry.grid(row=1, column=1, padx=10, pady=5)

        self.encrypt_key_label = tk.Label(
            self.encrypt_content, text="Key:", font=("Helvetica", 12))
        self.encrypt_key_label.grid(row=2, column=0, padx=10, pady=5)

        self.encrypt_key_entry = tk.Entry(
            self.encrypt_content, width=40, font=("Helvetica", 12))
        self.encrypt_key_entry.grid(row=2, column=1, padx=10, pady=5)

        self.encrypt_button = tk.Button(self.encrypt_content, text="Mã hóa", font=(
            "Helvetica", 12), command=self.encrypt_text)
        self.encrypt_button.grid(
            row=3, column=0, columnspan=2, padx=10, pady=10)

        self.encrypt_result_label = tk.Label(
            self.encrypt_content, text="Text đã mã hóa:", font=("Helvetica", 12))
        self.encrypt_result_label.grid(row=4, column=0, padx=10, pady=5)

        self.encrypt_result_text = tk.Text(
            self.encrypt_content, height=5, width=40, font=("Helvetica", 12))
        self.encrypt_result_text.grid(row=4, column=1, padx=10, pady=5)

        self.encrypt_copy_button = tk.Button(self.encrypt_content, text="Copy", font=(
            "Helvetica", 12), command=self.copy_encrypt_text)
        self.encrypt_copy_button.grid(row=5, column=1, padx=10, pady=10)

        # tạo nội dung cho phần Decrypt
        self.decrypt_content = tk.Frame(self.content, bg="#fff")
        self.decrypt_label = tk.Label(
            self.decrypt_content, text="Giải mã text đã mã hóa với key tương ứng", font=("Helvetica", 14))
        self.decrypt_label.grid(
            row=0, column=0, columnspan=2, padx=10, pady=10)

        self.decrypt_text_label = tk.Label(
            self.decrypt_content, text="Text đã mã hóa:", font=("Helvetica", 12))
        self.decrypt_text_label.grid(row=1, column=0, padx=10, pady=5)

        self.decrypt_text_entry = tk.Entry(
            self.decrypt_content, width=40, font=("Helvetica", 12))
        self.decrypt_text_entry.grid(row=1, column=1, padx=10, pady=5)

        self.decrypt_key_label = tk.Label(
            self.decrypt_content, text="Key:", font=("Helvetica", 12))
        self.decrypt_key_label.grid(row=2, column=0, padx=10, pady=5)

        self.decrypt_key_entry = tk.Entry(
            self.decrypt_content, width=40, font=("Helvetica", 12))
        self.decrypt_key_entry.grid(row=2, column=1, padx=10, pady=5)

        self.decrypt_button = tk.Button(self.decrypt_content, text="Giải mã", font=(
            "Helvetica", 12), command=self.decrypt_text)
        self.decrypt_button.grid(
            row=3, column=0, columnspan=2, padx=10, pady=10)

        self.decrypt_result_label = tk.Label(
            self.decrypt_content, text="Text đã giải mã:", font=("Helvetica", 12))
        self.decrypt_result_label.grid(row=4, column=0, padx=10, pady=5)

        self.decrypt_result_text = tk.Text(
            self.decrypt_content, height=5, width=40, font=("Helvetica", 12))
        self.decrypt_result_text.grid(row=4, column=1, padx=10, pady=5)

        self.decrypt_copy_button = tk.Button(self.decrypt_content, text="Copy", font=(
            "Helvetica", 12), command=self.copy_decrypt_text)
        self.decrypt_copy_button.grid(row=5, column=1, padx=10, pady=10)

 


    def show_encrypt(self):
        self.encrypt_content.pack()

    def show_decrypt(self):
        self.decrypt_content.pack()

    def encrypt_text(self):
        text = self.encrypt_text_entry.get()
        key = self.encrypt_key_entry.get()
        if text and key:
            aes = AESCipher(key)
            encrypted_text = aes.encrypt(text)
            self.encrypt_result_text.delete(1.0, tk.END)
            self.encrypt_result_text.insert(tk.END, encrypted_text)

    def copy_encrypt_text(self):
        encrypted_text = self.encrypt_result_text.get(1.0, tk.END)
        self.clipboard_clear()
        self.clipboard_append(encrypted_text)

    def decrypt_text(self):
        text = self.decrypt_text_entry.get()
        key = self.decrypt_key_entry.get()

        if text and key:
            aes = AESCipher(key)
            decrypted_text = aes.decrypt(text)
            self.decrypt_result_text.delete(1.0, tk.END)
            self.decrypt_result_text.insert(tk.END, decrypted_text)

    def copy_decrypt_text(self):
        decrypted_text = self.decrypt_result_text.get(1.0, tk.END)
        self.clipboard_clear()
        self.clipboard_append(decrypted_text)