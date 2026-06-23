import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sqlite3
import os
import shutil
from PIL import Image, ImageTk

from database import init_db, get_connection, update_record_count
from login import LoginWindow
from register import RegisterWindow
from reports import get_report_data
from charts import generate_charts
from security_doc import get_security_text

class SmartNotebookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Caderno Eletrônico em Python")
        self.root.geometry("950x650")
        self.root.configure(bg="#F8F9FA")
        self.is_authenticated = False
        self.selected_image_path = ""
        
        init_db()
        if not os.path.exists("attachments"):
            os.makedirs("attachments")
            
        self.build_welcome_view()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def build_welcome_view(self):
        self.clear_screen()
        self.root.configure(bg="#F8F9FA")
        
        title = tk.Label(self.root, text="Caderno Eletrônico em Python", font=("Segoe UI", 20, "bold"), fg="#1A1D20", bg="#F8F9FA")
        title.pack(pady=35)
        
        desc_text = "Projeto Técnico\nRede de Computadores  •  Segurança da Informação  •  Linguagens para Banco de Dados  •  Planejamento e Prática Profissional"
        desc = tk.Label(self.root, text=desc_text, font=("Segoe UI", 10), fg="#5A626A", justify="center", bg="#F8F9FA")
        desc.pack(pady=10)

        btn_frame = tk.Frame(self.root, bg="#F8F9FA")
        btn_frame.pack(pady=30)
        
        btn_login = tk.Button(btn_frame, text="Entrar (Login)", width=16, font=("Segoe UI", 11, "bold"), bg="#2B8A3E", fg="white", bd=0, cursor="hand2", pady=8, command=self.trigger_login)
        btn_login.grid(row=0, column=0, padx=15)
        
        btn_reg = tk.Button(btn_frame, text="Cadastrar", width=16, font=("Segoe UI", 11, "bold"), bg="#1C7ED6", fg="white", bd=0, cursor="hand2", pady=8, command=self.trigger_register)
        btn_reg.grid(row=0, column=1, padx=15)
        
        about_box = tk.LabelFrame(self.root, text=" Credenciais do Projeto ", font=("Segoe UI", 9, "bold"), fg="#495057", bg="#F8F9FA", padx=20, pady=15, bd=1, relief="solid")
        about_box.pack(pady=30, fill="x", padx=60)
        
        metadata = "Desenvolvedor: Gustavo Thenório Cavalcante\nCurso:         3° Informática"
        tk.Label(about_box, text=metadata, justify="left", font=("Consolas", 11), fg="#212529", bg="#F8F9FA").pack(anchor="w")

        btn_exit = tk.Button(self.root, text="Sair do Sistema", font=("Segoe UI", 9), bg="#E03131", fg="white", bd=0, cursor="hand2", pady=5, command=self.root.quit)
        btn_exit.pack(side="bottom", pady=20)

    def trigger_login(self):
        LoginWindow(self.root, self.login_success)

    def trigger_register(self):
        RegisterWindow(self.root)

    def login_success(self):
        self.is_authenticated = True
        self.build_dashboard_view()

    def build_dashboard_view(self):
        self.clear_screen()
        
        last_note_date = "Nenhuma anotação"
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT date FROM activities ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            if row:
                raw_date = row[0]
                if "-" in raw_date:
                    parts = raw_date.split("-")
                    last_note_date = f"{parts[2]}/{parts[1]}/{parts[0]}"
                else:
                    last_note_date = raw_date
            conn.close()
        except Exception:
            last_note_date = "Erro ao ler banco"

        nav_frame = tk.Frame(self.root, bg="#2A2F35", bd=0)
        nav_frame.pack(side="left", fill="y")
        
        user_panel = tk.Frame(nav_frame, bg="#1E2226", pady=15, padx=15)
        user_panel.pack(fill="x", side="top")
        
        lbl_user = tk.Label(user_panel, text="Bem-vindo, Gustavo", font=("Segoe UI", 11, "bold"), fg="#FFFFFF", bg="#1E2226", anchor="w")
        lbl_user.pack(fill="x")
        
        lbl_access = tk.Label(user_panel, text=f"Última anotação: {last_note_date}", font=("Segoe UI", 8), fg="#ADB5BD", bg="#1E2226", anchor="w")
        lbl_access.pack(fill="x", pady=(2, 0))
        
        tk.Frame(nav_frame, height=1, bg="#3A4149").pack(fill="x", pady=(0, 10))
        
        buttons_info = [
            ("Registrar Dados", self.view_data_entry),
            ("Visualizar Banco", self.view_database_records),
            ("Gerar Relatórios", self.view_reports_panel),
            ("Gráficos Estatísticos", self.view_charts_panel),
            ("Eng. de Software", self.view_swe_theory),
            ("Segurança da Info.", self.view_security_panel)
        ]
        
        for text, command in buttons_info:
            is_bold = "Gráficos" in text or "Registrar" in text
            btn = tk.Button(
                nav_frame, text=text, font=("Segoe UI", 10, "bold" if is_bold else "normal"),
                bg="#2A2F35", fg="#E9ECEF", activebackground="#3A4149", activeforeground="#FFFFFF",
                bd=0, anchor="w", padx=18, pady=8, cursor="hand2", command=command
            )
            btn.pack(fill="x", pady=1)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#343A40"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#2A2F35"))
            
        btn_logout = tk.Button(nav_frame, text="Fazer Logout", font=("Segoe UI", 9, "bold"), bg="#E67E22", fg="white", bd=0, cursor="hand2", pady=6, command=self.build_welcome_view)
        btn_logout.pack(side="bottom", fill="x", pady=15, padx=10)

        self.work_canvas = tk.Frame(self.root, bg="#FFFFFF", bd=0)
        self.work_canvas.pack(side="right", expand=True, fill="both", padx=15, pady=15)
        
        tk.Label(self.work_canvas, text="Painel Ativo", font=("Segoe UI", 16, "bold"), fg="#212529", bg="#FFFFFF").pack(pady=30)
        tk.Label(self.work_canvas, text="Selecione uma opção no menu lateral para começar.", font=("Segoe UI", 11), fg="#6C757D", bg="#FFFFFF").pack()

    def clear_work_canvas(self):
        for widget in self.work_canvas.winfo_children():
            widget.destroy()

    def select_image_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif")])
        if file_path:
            self.selected_image_path = file_path
            filename = os.path.basename(file_path)
            self.lbl_img_status.config(text=f"Selecionado: {filename[:20]}...", fg="#2B8A3E")

    def view_data_entry(self):
        self.clear_work_canvas()
        self.selected_image_path = ""
        
        tk.Label(self.work_canvas, text="Registrar Nova Atividade Acadêmica", font=("Segoe UI", 14, "bold"), fg="#212529", bg="#FFFFFF").pack(pady=15)
        
        form_frame = tk.Frame(self.work_canvas, bg="#FFFFFF")
        form_frame.pack(pady=10)
        
        tk.Label(form_frame, text="Matéria:", font=("Segoe UI", 10, "bold"), fg="#495057", bg="#FFFFFF").pack(anchor="w", pady=(5, 2))
        self.cb_subject = ttk.Combobox(form_frame, values=["Rede de Computadores", "Segurança da Informação", "Linguagens para Banco de Dados", "Planejamento e Prática Profissional"], width=40, state="readonly")
        self.cb_subject.pack(pady=5)
        self.cb_subject.current(0)
        
        tk.Label(form_frame, text="Descrição da Atividade / Anotações:", font=("Segoe UI", 10, "bold"), fg="#495057", bg="#FFFFFF").pack(anchor="w", pady=(10, 2))
        self.txt_activity = tk.Text(form_frame, height=5, width=40, font=("Segoe UI", 10), bd=1, relief="solid")
        self.txt_activity.pack(pady=5)
        
        tk.Label(form_frame, text="Data (AAAA-MM-DD):", font=("Segoe UI", 10, "bold"), fg="#495057", bg="#FFFFFF").pack(anchor="w", pady=(10, 2))
        self.ent_date = tk.Entry(form_frame, font=("Segoe UI", 10), width=42, bd=1, relief="solid")
        self.ent_date.insert(0, "2026-06-23")
        self.ent_date.pack(pady=5)
        
        tk.Label(form_frame, text="Print da Lição (Opcional):", font=("Segoe UI", 10, "bold"), fg="#495057", bg="#FFFFFF").pack(anchor="w", pady=(10, 2))
        btn_img = tk.Button(form_frame, text="Escolher Imagem...", font=("Segoe UI", 9), bg="#495057", fg="white", bd=0, cursor="hand2", pady=4, padx=10, command=self.select_image_file)
        btn_img.pack(anchor="w", pady=2)
        
        self.lbl_img_status = tk.Label(form_frame, text="Nenhuma imagem anexada", font=("Segoe UI", 9, "italic"), fg="#868E96", bg="#FFFFFF")
        self.lbl_img_status.pack(anchor="w")
        
        tk.Button(self.work_canvas, text="Salvar no Banco", font=("Segoe UI", 11, "bold"), bg="#2B8A3E", fg="white", bd=0, cursor="hand2", pady=8, padx=15, command=self.save_activity_log).pack(pady=20)

    def save_activity_log(self):
        subject = self.cb_subject.get()
        activity = self.txt_activity.get("1.0", tk.END).strip()
        date = self.ent_date.get().strip()
        
        if not activity or not date:
            messagebox.showerror("Erro", "Todos os campos precisam ser preenchidos.")
            return
            
        saved_db_path = ""
        if self.selected_image_path:
            try:
                ext = os.path.splitext(self.selected_image_path)[1]
                new_filename = f"img_{int(os.path.getmtime(self.selected_image_path))}{ext}"
                dest_path = os.path.join("attachments", new_filename)
                shutil.copy(self.selected_image_path, dest_path)
                saved_db_path = dest_path
            except Exception as e:
                messagebox.showerror("Erro de Arquivo", f"Não foi possível salvar a imagem: {str(e)}")
                return
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO activities (subject, activity, date, image_path) VALUES (?, ?, ?, ?)", (subject, activity, date, saved_db_path))
            conn.commit()
            conn.close()
            update_record_count()
            messagebox.showinfo("Sucesso", "Dados salvos com sucesso.")
            self.txt_activity.delete("1.0", tk.END)
            self.build_dashboard_view()  
            self.view_data_entry()       
        except Exception as e:
            messagebox.showerror("Erro no Banco", f"Falha ao salvar: {str(e)}")

    def view_database_records(self):
        self.clear_work_canvas()
        tk.Label(self.work_canvas, text="Visualizador do Banco de Dados", font=("Segoe UI", 14, "bold"), fg="#212529", bg="#FFFFFF").pack(pady=10)
        
        split_frame = tk.Frame(self.work_canvas, bg="#FFFFFF")
        split_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        left_box = tk.Frame(split_frame, bg="#FFFFFF")
        left_box.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.records_list = tk.Listbox(left_box, font=("Consolas", 10), bd=1, relief="solid", highlightthickness=0)
        self.records_list.pack(side="left", fill="both", expand=True)
        self.records_list.bind("<<ListboxSelect>>", self.on_record_select)
        
        scroll = tk.Scrollbar(left_box, command=self.records_list.yview)
        scroll.pack(side="right", fill="y")
        self.records_list.config(yscrollcommand=scroll.set)
        
        self.right_preview = tk.Frame(split_frame, bg="#F1F3F5", width=320, bd=1, relief="solid")
        self.right_preview.pack(side="right", fill="both", expand=False)
        self.right_preview.pack_propagate(False)
        
        self.btn_view_image = tk.Button(
            self.right_preview, text="🔍 Ver Print Anexado", font=("Segoe UI", 10, "bold"),
            bg="#718096", fg="white", bd=0, cursor="hand2", pady=8, state="disabled",
            command=self.open_full_screen_image
        )
        self.btn_view_image.pack(fill="x", padx=10, pady=10)
        
        tk.Frame(self.right_preview, height=1, bg="#CED4DA").pack(fill="x", pady=5)
        
        tk.Label(self.right_preview, text="Anotação Completa:", font=("Segoe UI", 10, "bold"), fg="#495057", bg="#F1F3F5").pack(anchor="w", padx=10, pady=(5, 2))
        
        text_frame = tk.Frame(self.right_preview, bg="#F1F3F5")
        text_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.txt_full_activity = tk.Text(text_frame, font=("Segoe UI", 10), bg="#FFFFFF", bd=1, relief="solid", wrap="word")
        self.txt_full_activity.pack(side="left", fill="both", expand=True)
        
        txt_scroll = tk.Scrollbar(text_frame, command=self.txt_full_activity.yview)
        txt_scroll.pack(side="right", fill="y")
        self.txt_full_activity.config(yscrollcommand=txt_scroll.set)
        self.txt_full_activity.insert("1.0", "Selecione um item para ler o conteúdo completo.")
        self.txt_full_activity.config(state="disabled")
        
        ctrl_frame = tk.Frame(self.work_canvas, bg="#FFFFFF")
        ctrl_frame.pack(fill="x", pady=10)
        tk.Button(ctrl_frame, text="Excluir Registro Selecionado", font=("Segoe UI", 10, "bold"), bg="#C92A2A", fg="white", bd=0, cursor="hand2", pady=6, padx=12, command=self.delete_selected_record).pack(side="left", padx=10)
        
        self.refresh_records_view()

    def on_record_select(self, event):
        try:
            selected_index = self.records_list.curselection()[0]
            
            full_text = self.loaded_records_data[selected_index][3]
            self.current_selected_img_path = self.loaded_records_data[selected_index][4]
            
            self.txt_full_activity.config(state="normal")
            self.txt_full_activity.delete("1.0", tk.END)
            self.txt_full_activity.insert("1.0", full_text)
            self.txt_full_activity.config(state="disabled")
            
            if self.current_selected_img_path and os.path.exists(self.current_selected_img_path):
                self.btn_view_image.config(state="normal", bg="#3182CE", text="🔍 Ver Print Anexado (Disponível)")
            else:
                self.btn_view_image.config(state="disabled", bg="#718096", text="❌ Sem Print Anexado")
        except IndexError:
            pass

    def open_full_screen_image(self):
        if hasattr(self, 'current_selected_img_path') and os.path.exists(self.current_selected_img_path):
            full_window = tk.Toplevel(self.root)
            full_window.title("Visualização do Print do Classroom")
            full_window.geometry("1024x768")
            full_window.configure(bg="#1A202C")
            
            img_original = Image.open(self.current_selected_img_path)
            img_original.thumbnail((1000, 720), Image.Resampling.LANCZOS)
            photo_full = ImageTk.PhotoImage(img_original)
            
            lbl_full = tk.Label(full_window, image=photo_full, bg="#1A202C")
            lbl_full.image = photo_full 
            lbl_full.pack(expand=True, fill="both", padx=10, pady=10)

    def refresh_records_view(self):
        self.records_list.delete(0, tk.END)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, subject, date, activity, image_path FROM activities")
        self.loaded_records_data = cursor.fetchall()
        conn.close()
        
        for row in self.loaded_records_data:
            has_img = "[IMG] " if row[4] else ""
            summary = f"ID: {row[0]:<3} | {has_img}[{row[1]}] ({row[2]}) -> {row[3][:25]}"
            self.records_list.insert(tk.END, summary)

    def delete_selected_record(self):
        try:
            selected_index = self.records_list.curselection()[0]
            record_id = self.loaded_records_data[selected_index][0]
            img_path = self.loaded_records_data[selected_index][4]
            
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM activities WHERE id = ?", (record_id,))
            conn.commit()
            conn.close()
            
            if img_path and os.path.exists(img_path):
                try:
                    os.remove(img_path)
                except Exception:
                    pass
            
            update_record_count()
            self.build_dashboard_view()  
            self.view_database_records() 
            messagebox.showinfo("Sucesso", "Registro removido com sucesso.")
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione uma linha para excluir.")

    def view_reports_panel(self):
        self.clear_work_canvas()
        tk.Label(self.work_canvas, text="Estatísticas e Relatórios Gerais", font=("Segoe UI", 14, "bold"), fg="#212529", bg="#FFFFFF").pack(pady=10)
        
        report_data = get_report_data()
        
        display_box = tk.Text(self.work_canvas, height=14, width=58, font=("Consolas", 10), bg="#F1F3F5", bd=1, relief="solid", padx=10, pady=10)
        display_box.insert("1.0", report_data)
        display_box.config(state="disabled")
        display_box.pack(pady=10)

    def view_charts_panel(self):
        self.clear_work_canvas()
        tk.Label(self.work_canvas, text="Integração de Gráficos Matplotlib", font=("Segoe UI", 14, "bold"), fg="#212529", bg="#FFFFFF").pack(pady=10)
        
        success = generate_charts()
        if not success:
            tk.Label(self.work_canvas, text="Insira dados no caderno antes de gerar os gráficos.", font=("Segoe UI", 11), fg="#E67E22", bg="#FFFFFF").pack(pady=20)
            return
            
        tk.Label(self.work_canvas, text="Métricas consolidadas em tempo real:", font=("Segoe UI", 10), fg="#495057", bg="#FFFFFF").pack(pady=5)
        
        img_frame = tk.Frame(self.work_canvas, bg="#FFFFFF")
        img_frame.pack(fill="x", expand=True, pady=5)
        
        img_frame.grid_columnconfigure(0, weight=1)
        img_frame.grid_columnconfigure(1, weight=1)
        
        try:
            img_bar = Image.open("charts_bar.png")
            img_bar = img_bar.resize((340, 280), Image.Resampling.LANCZOS)
            self.photo_bar = ImageTk.PhotoImage(img_bar)
            lbl_bar = tk.Label(img_frame, image=self.photo_bar, bg="#FFFFFF")
            lbl_bar.grid(row=0, column=0, padx=10, pady=5, sticky="e")
            
            img_pie = Image.open("charts_pie.png")
            img_pie = img_pie.resize((340, 280), Image.Resampling.LANCZOS)
            self.photo_pie = ImageTk.PhotoImage(img_pie)
            lbl_pie = tk.Label(img_frame, image=self.photo_pie, bg="#FFFFFF")
            lbl_pie.grid(row=0, column=1, padx=10, pady=5, sticky="w")
            
        except Exception as e:
            tk.Label(self.work_canvas, text=f"Erro ao renderizar imagens: {str(e)}", fg="orange", bg="#FFFFFF").pack()
        
        tk.Button(self.work_canvas, text="Atualizar Dados", font=("Segoe UI", 10, "bold"), bg="#1C7ED6", fg="white", bd=0, cursor="hand2", pady=6, padx=12, command=self.view_charts_panel).pack(pady=10)

    def view_swe_theory(self):
        self.clear_work_canvas()
        tk.Label(self.work_canvas, text="Conceitos de Engenharia de Software", font=("Segoe UI", 14, "bold"), fg="#212529", bg="#FFFFFF").pack(pady=5)
        
        swe_content = """=== Planejamento e Arquitetura do Sistema ===
- Padrão Arquitetural: Design Estrutural Modular.
- Divisão de Camadas: Separação de responsabilidades com interface visual (login.py, register.py), lógica de banco (database.py), segurança (security.py) e processamento (charts.py, reports.py).

=== Diagrama Estrutural ===
+-------------------------------------------------------+
|                       main.py                         |
+-------------------------------------------------------+
   |          |             |              |          |
   v          v             v              v          v
[login]  [register]    [database]      [charts]   [reports]
                            |
                            v
                      [notebook.db]
"""
        txt = tk.Text(self.work_canvas, height=16, width=58, font=("Consolas", 9), bg="#F1F3F5", bd=1, relief="solid", padx=10, pady=10)
        txt.insert("1.0", swe_content)
        txt.config(state="disabled")
        txt.pack()

    def view_security_panel(self):
        self.clear_work_canvas()
        tk.Label(self.work_canvas, text="Segurança e Proteção de Dados", font=("Segoe UI", 14, "bold"), fg="#212529", bg="#FFFFFF").pack(pady=5)
        
        txt = tk.Text(self.work_canvas, height=16, width=58, font=("Consolas", 9), bg="#F1F3F5", bd=1, relief="solid", padx=10, pady=10)
        txt.insert("1.0", get_security_text())
        txt.config(state="disabled")
        txt.pack()

if __name__ == "__main__":
    window_manager = tk.Tk()
    app_instance = SmartNotebookApp(window_manager)
    window_manager.mainloop()