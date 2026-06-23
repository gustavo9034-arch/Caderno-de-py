import tkinter as tk
from tkinter import messagebox
import sqlite3
from database import get_connection, increment_access
from security import hash_password, validate_input

class LoginWindow:
    def __init__(self, root, login_success_callback):
        self.root = root
        self.callback = login_success_callback
        self.top = tk.Toplevel(root)
        self.top.title("Acesso ao Sistema")
        self.top.geometry("350x250")
        
        tk.Label(self.top, text="Entrar", font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(self.top, text="Usuário:").pack()
        self.ent_username = tk.Entry(self.top)
        self.ent_username.pack(pady=2)
        
        tk.Label(self.top, text="Senha:").pack()
        self.ent_password = tk.Entry(self.top, show="*")
        self.ent_password.pack(pady=2)
        
        tk.Button(self.top, text="Login", width=15, bg="#4CAF50", fg="white", command=self.attempt_login).pack(pady=15)
        
    def attempt_login(self):
        user = validate_input(self.ent_username.get())
        pwd = validate_input(self.ent_password.get())
        
        if not user or not pwd:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return
            
        hashed_pwd = hash_password(pwd)
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user, hashed_pwd))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            messagebox.showinfo("Sucesso", f"Bem-vindo de volta, {result[1]}!")
            increment_access()
            self.top.destroy()
            self.callback()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")