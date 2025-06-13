import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
from pathlib import Path
from consolidacao import listar_arquivos_python, processar_arquivos

class ConsolidadorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Consolidador de Código Python")
        self.root.geometry("900x600")
        self.root.resizable(width=False, height=False)
        self.root.configure(bg='#1a1a1a')

        self.pasta_selecionada = tk.StringVar()
        self.caminho_saida = tk.StringVar()
        self.modo_saida = tk.StringVar(value="unique")
        self.arquivos_encontrados = []
        self.checkboxes_arquivos = {}

        desktop_path = Path.home() / "Desktop" / "codigo_consolidado.txt"
        self.caminho_saida.set(str(desktop_path))

        self.criar_interface()

    def criar_interface(self):
        main_container = tk.Frame(self.root, bg='#1a1a1a')
        main_container.pack(fill='both', expand=True, padx=15, pady=15)

        self.criar_painel_lateral(main_container)
        separador = tk.Frame(main_container, bg='#404040', width=2)
        separador.pack(side='left', fill='y', padx=8)
        self.criar_painel_principal(main_container)

    def criar_painel_lateral(self, parent):
        lateral_frame = tk.Frame(parent, bg='#2d2d2d', width=320)
        lateral_frame.pack(side='left', fill='y')
        lateral_frame.pack_propagate(False)

        header = tk.Label(lateral_frame, text="Arquivos Python Encontrados", font=("Segoe UI", 13, "bold"), fg='#61dafb', bg='#2d2d2d')
        header.pack(pady=(18, 10))

        botoes_frame = tk.Frame(lateral_frame, bg='#2d2d2d')
        botoes_frame.pack(fill='x', padx=15, pady=8)
        tk.Button(botoes_frame, text="Marcar Todos", command=self.selecionar_todos, bg='#4CAF50', fg='white', font=("Segoe UI", 9, "bold"), relief='flat', cursor='hand2').pack(side='left', expand=True, fill='x', padx=(0, 4))
        tk.Button(botoes_frame, text="Desmarcar Todos", command=self.desmarcar_todos, bg='#f44336', fg='white', font=("Segoe UI", 9, "bold"), relief='flat', cursor='hand2').pack(side='right', expand=True, fill='x', padx=(4, 0))

        scroll_container = tk.Frame(lateral_frame, bg='#1e1e1e')
        scroll_container.pack(fill='both', expand=True, padx=15, pady=5)
        self.canvas_arquivos = tk.Canvas(scroll_container, bg='#1e1e1e', highlightthickness=0)
        scrollbar_arquivos = ttk.Scrollbar(scroll_container, orient="vertical", command=self.canvas_arquivos.yview)
        self.frame_arquivos = tk.Frame(self.canvas_arquivos, bg='#1e1e1e')
        self.canvas_arquivos.configure(yscrollcommand=scrollbar_arquivos.set)
        self.canvas_arquivos.create_window((0, 0), window=self.frame_arquivos, anchor="nw")
        self.frame_arquivos.bind("<Configure>", lambda e: self.canvas_arquivos.configure(scrollregion=self.canvas_arquivos.bbox("all")))
        self.canvas_arquivos.pack(side="left", fill="both", expand=True)
        scrollbar_arquivos.pack(side="right", fill="y")

        contador_frame = tk.Frame(lateral_frame, bg='#2d2d2d')
        contador_frame.pack(fill='x', padx=15, pady=10)
        self.label_contador = tk.Label(contador_frame, text="Nenhum arquivo encontrado", font=("Segoe UI", 10, "bold"), fg='#61dafb', bg='#2d2d2d')
        self.label_contador.pack()

    def criar_painel_principal(self, parent):
        principal_frame = tk.Frame(parent, bg='#1a1a1a')
        principal_frame.pack(side='right', fill='both', expand=True)

        tk.Label(principal_frame, text="Consolidador Python", font=("Segoe UI", 18, "bold"), fg='#61dafb', bg='#1a1a1a').pack(pady=(10, 0))
        tk.Label(principal_frame, text="Unifique ou exporte seus arquivos Python com um clique.", font=("Segoe UI", 10), fg='#b0b0b0', bg='#1a1a1a').pack()

        config_frame = tk.Frame(principal_frame, bg='#1a1a1a')
        config_frame.pack(fill='x', padx=20, pady=20)

        # Pasta do Projeto
        pasta_section = tk.Frame(config_frame, bg='#2d2d2d', relief='flat', bd=1)
        pasta_section.pack(fill='x', pady=(0, 6), ipady=10, ipadx=10)
        tk.Label(pasta_section, text="Pasta do Projeto", font=("Segoe UI", 12, "bold"), fg="white", bg="#2d2d2d").pack(anchor='w', padx=10, pady=(0, 5))
        pasta_input_frame = tk.Frame(pasta_section, bg="#2d2d2d")
        pasta_input_frame.pack(fill='x', padx=10)
        self.pasta_entry = tk.Entry(pasta_input_frame, textvariable=self.pasta_selecionada, font=("Segoe UI", 10), bg='#404040', fg='white', relief='flat', insertbackground='white')
        self.pasta_entry.pack(side='left', fill='x', expand=True, ipady=5)
        tk.Button(pasta_input_frame, text="Procurar...", command=self.selecionar_pasta, bg='#61dafb', fg='black', font=("Segoe UI", 10, "bold"), relief='flat', cursor='hand2').pack(side='right', padx=(8, 0))

        # Arquivo/Pasta de Saída
        saida_section = tk.Frame(config_frame, bg='#2d2d2d', relief='flat', bd=1)
        saida_section.pack(fill='x', pady=(0, 6), ipady=10, ipadx=10)
        self.label_saida = tk.Label(saida_section, text="Arquivo de Saída", font=("Segoe UI", 12, "bold"), fg="white", bg="#2d2d2d")
        self.label_saida.pack(anchor='w', padx=10, pady=(0, 5))
        saida_input_frame = tk.Frame(saida_section, bg="#2d2d2d")
        saida_input_frame.pack(fill='x', padx=10)
        self.saida_entry = tk.Entry(saida_input_frame, textvariable=self.caminho_saida, font=("Segoe UI", 10), bg='#404040', fg='white', relief='flat', insertbackground='white')
        self.saida_entry.pack(side='left', fill='x', expand=True, ipady=5)
        self.btn_procurar_saida = tk.Button(saida_input_frame, text="Salvar Como...", command=self.selecionar_caminho_saida, bg='#ff9800', fg='black', font=("Segoe UI", 10, "bold"), relief='flat', cursor='hand2')
        self.btn_procurar_saida.pack(side='right', padx=(8, 0))

        # Opções de Saída
        opcoes_section = tk.Frame(config_frame, bg='#2d2d2d', relief='flat', bd=1)
        opcoes_section.pack(fill='x', pady=(0, 6), ipady=10, ipadx=10)
        tk.Label(opcoes_section, text="Opções de Saída", font=("Segoe UI", 12, "bold"), fg="white", bg="#2d2d2d").pack(anchor='w', padx=10, pady=(0, 8))
        opcoes_input_frame = tk.Frame(opcoes_section, bg="#2d2d2d")
        opcoes_input_frame.pack(fill='x', padx=10)
        ttk.Style().configure("TRadiobutton", background="#2d2d2d", foreground="white", font=("Segoe UI", 10), padding=5)
        rb_unique = ttk.Radiobutton(opcoes_input_frame, text="Arquivo Único", variable=self.modo_saida, value="unique", command=self.atualizar_saida, style="TRadiobutton", cursor='hand2')
        rb_unique.pack(side='left', padx=(0, 20))
        rb_split = ttk.Radiobutton(opcoes_input_frame, text="Arquivos Separados", variable=self.modo_saida, value="split", command=self.atualizar_saida, style="TRadiobutton", cursor='hand2')
        rb_split.pack(side='left')

        # Botão de consolidar
        self.btn_consolidar = tk.Button(principal_frame, text="CONSOLIDAR ARQUIVOS", command=self.iniciar_consolidacao, bg='#4CAF50', fg='white', font=("Segoe UI", 12, "bold"), relief='flat', cursor='hand2', pady=10)
        self.btn_consolidar.pack(fill='x', padx=20, pady=10)

        # Log de processamento
        log_section = tk.Frame(principal_frame, bg='#1a1a1a')
        log_section.pack(fill='both', expand=True, padx=20, pady=5)
        tk.Label(log_section, text="Log de Processamento", font=("Segoe UI", 12, "bold"), fg="white", bg="#1a1a1a").pack(anchor='w')
        self.log_text = scrolledtext.ScrolledText(log_section, height=6, bg='#1e1e1e', fg='#00ff41', font=("Consolas", 9), relief='flat', bd=1, highlightthickness=1, highlightbackground='#404040', insertbackground='white')
        self.log_text.pack(fill='both', expand=True, pady=(5,0))

        # Rodapé
        footer_frame = tk.Frame(principal_frame, bg='#1a1a1a')
        footer_frame.pack(fill='x', padx=20, pady=10)
        ttk.Style().configure("Custom.Horizontal.TProgressbar", background='#4CAF50', troughcolor='#404040', borderwidth=0)
        self.progress = ttk.Progressbar(footer_frame, mode='indeterminate', style="Custom.Horizontal.TProgressbar")
        self.progress.pack(fill='x', pady=(0, 8))
        tk.Label(footer_frame, text="Desenvolvido por Comunidade DEV", font=("Segoe UI", 8, "italic"), fg='#888888', bg='#1a1a1a').pack()

    def atualizar_saida(self):
        modo = self.modo_saida.get()
        if modo == "unique":
            self.label_saida.config(text="Arquivo de Saída")
            self.btn_procurar_saida.config(text="Salvar Como...")
            current_path = self.caminho_saida.get()
            if os.path.isdir(current_path):
                self.caminho_saida.set(str(Path(current_path) / "codigo_consolidado.txt"))
        elif modo == "split":
            self.label_saida.config(text="Pasta de Saída")
            self.btn_procurar_saida.config(text="Selecionar Pasta")
            current_path = Path(self.caminho_saida.get())
            if current_path.suffix:
                self.caminho_saida.set(str(current_path.parent))

    def selecionar_pasta(self):
        pasta = filedialog.askdirectory(title="Selecione a pasta do projeto")
        if pasta:
            self.pasta_selecionada.set(pasta)
            self.carregar_arquivos_python()

    def selecionar_caminho_saida(self):
        modo = self.modo_saida.get()
        initial_dir = str(Path(self.caminho_saida.get()).parent)
        if modo == "unique":
            arquivo = filedialog.asksaveasfilename(
                title="Salvar arquivo consolidado como...",
                defaultextension=".txt",
                filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")],
                initialdir=initial_dir,
                initialfile="codigo_consolidado.txt"
            )
            if arquivo:
                self.caminho_saida.set(arquivo)
        elif modo == "split":
            pasta = filedialog.askdirectory(
                title="Selecione a pasta de saída para os arquivos",
                initialdir=initial_dir
            )
            if pasta:
                self.caminho_saida.set(pasta)

    def carregar_arquivos_python(self):
        for widget in self.frame_arquivos.winfo_children():
            widget.destroy()
        self.checkboxes_arquivos.clear()
        pasta = self.pasta_selecionada.get()
        if not pasta or not os.path.exists(pasta):
            return
        self.arquivos_encontrados = listar_arquivos_python(pasta)
        if not self.arquivos_encontrados:
            tk.Label(self.frame_arquivos, text="Nenhum arquivo Python encontrado.", font=("Segoe UI", 10), fg='#888888', bg='#1e1e1e').pack(pady=30)
        else:
            for i, arquivoinfo in enumerate(self.arquivos_encontrados):
                var = tk.BooleanVar(value=True)
                frame_checkbox = tk.Frame(self.frame_arquivos, bg='#1e1e1e')
                frame_checkbox.pack(fill='x', padx=5, pady=1)
                check = tk.Checkbutton(frame_checkbox, text=str(arquivoinfo['caminhorelativo']), variable=var,
                                       bg='#1e1e1e', fg='white', selectcolor='#404040', activebackground='#2d2d2d',
                                       activeforeground='#61dafb', font=("Segoe UI", 9), anchor='w', justify='left',
                                       relief='flat', command=self.atualizar_contador, cursor='hand2')
                check.pack(fill='x', anchor='w', padx=4, pady=2)
                self.checkboxes_arquivos[i] = {'var': var, 'checkbox': check, 'arquivoinfo': arquivoinfo}
        self.atualizar_contador()
        self.log(f"Encontrados {len(self.arquivos_encontrados)} arquivos Python na pasta.\n")

    def selecionar_todos(self):
        for data in self.checkboxes_arquivos.values():
            data['var'].set(True)
        self.atualizar_contador()

    def desmarcar_todos(self):
        for data in self.checkboxes_arquivos.values():
            data['var'].set(False)
        self.atualizar_contador()

    def atualizar_contador(self):
        selecionados = sum(1 for data in self.checkboxes_arquivos.values() if data['var'].get())
        total = len(self.checkboxes_arquivos)
        self.label_contador.config(text=f"{selecionados} de {total} arquivos selecionados")

    def obter_arquivos_selecionados(self):
        return [data['arquivoinfo'] for data in self.checkboxes_arquivos.values() if data['var'].get()]

    def log(self, mensagem):
        self.log_text.insert(tk.END, mensagem)
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def iniciar_consolidacao(self):
        if not self.pasta_selecionada.get():
            messagebox.showwarning("Atenção", "Selecione uma pasta de projeto primeiro.")
            return
        arquivos_selecionados = self.obter_arquivos_selecionados()
        if not arquivos_selecionados:
            messagebox.showwarning("Atenção", "Selecione pelo menos um arquivo para consolidar.")
            return
        caminho_saida = self.caminho_saida.get()
        if not caminho_saida:
            messagebox.showwarning("Atenção", "Defina o caminho de saída.")
            return
        self.btn_consolidar.config(state='disabled', bg='#666666')
        self.progress.start(10)
        thread = threading.Thread(target=self.executar_consolidacao, args=(arquivos_selecionados, caminho_saida, self.modo_saida.get()))
        thread.daemon = True
        thread.start()

    def executar_consolidacao(self, arquivos_selecionados, caminho_saida, modo):
        self.log_text.delete('1.0', tk.END)
        self.log(f"Iniciando processamento no modo: '{'Arquivo Único' if modo == 'unique' else 'Arquivos Separados'}'\n")
        self.log(f"Pasta de origem: {self.pasta_selecionada.get()}\n")
        self.log(f"Caminho de destino: {caminho_saida}\n")
        self.log("-" * 60 + "\n")
        try:
            arquivos_processados = processar_arquivos(arquivos_selecionados, caminho_saida, modo)
            self.log("Arquivos processados com sucesso:\n")
            for arquivo in arquivos_selecionados:
                self.log(f"  - {arquivo['caminhorelativo']}\n")
            self.log("-" * 60 + "\n")
            if modo == "unique":
                msg = "Arquivo consolidado salvo com sucesso."
                local_msg = f"Local: {caminho_saida}"
            else:
                msg = "Arquivos exportados com sucesso para a pasta."
                local_msg = f"Pasta de destino: {caminho_saida}"
            self.log(f"{msg}\n")
            self.log(f"Total de arquivos processados: {arquivos_processados}\n")
            messagebox.showinfo("Sucesso.", f"{msg}\n{local_msg}\nTotal: {arquivos_processados} arquivos.")
        except Exception as e:
            self.log(f"\nERRO: {e}\n")
            messagebox.showerror("Erro", f"Ocorreu um erro durante o processamento:\n{e}")
        finally:
            self.progress.stop()
            self.btn_consolidar.config(state='normal', bg='#4CAF50')

def main():
    root = tk.Tk()
    app = ConsolidadorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
