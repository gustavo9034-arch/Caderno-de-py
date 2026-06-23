import tkinter as tk
from tkinter import messagebox
import sqlite3
from database import get_connection
from security import hash_password, validate_input

class RegisterWindow:
    def __init__(self, root):
        self.top = tk.Toplevel(root)
        self.top.title("Cadastro de Usuário")
        self.top.geometry("350x280")
        
        tk.Label(self.top, text="Criar Conta", font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(self.top, text="Nome Completo:").pack()
        self.ent_name = tk.Entry(self.top)
        self.ent_name.pack(pady=2)
        
        tk.Label(self.top, text="Nome de Usuário (Login):").pack()
        self.ent_user = tk.Entry(self.top)
        self.ent_user.pack(pady=2)
        
        tk.Label(self.top, text="Senha:").pack()
        self.ent_pwd = tk.Entry(self.top, show="*")
        self.ent_pwd.pack(pady=2)
        
        tk.Button(self.top, text="Cadastrar", width=15, bg="#2196F3", fg="white", command=self.save_user).pack(pady=15)
        
    def save_user(self):
        name = validate_input(self.ent_name.get())
        user = validate_input(self.ent_user.get())
        pwd = validate_input(self.ent_pwd.get())
        
        if not name or not user or not pwd:
            messagebox.showerror("Erro", "Campos vazios não são permitidos.")
            return
            
        hashed = hash_password(pwd)
        
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (name, username, password) VALUES (?, ?, ?)", (name, user, hashed))
            conn.commit()
            messagebox.showinfo("Sucesso", "Conta criada com sucesso!")
            self.top.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Este nome de usuário já existe.")
        finally:
            conn.close()