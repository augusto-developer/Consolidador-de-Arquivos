import tkinter as tk
from tkinter import ttk, scrolledtext

class PainelPrincipal(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg='#1a1a1a')
        self.controller = controller
        self.pack(side='right', fill='both', expand=True)
        self._criar_widgets()

    def _criar_widgets(self):
        tk.Label(self, text="Consolidador Python", font=("Segoe UI", 18, "bold"), fg='#61dafb', bg='#1a1a1a').pack(pady=(10, 0))
        tk.Label(self, text="Unifique ou exporte seus arquivos Python com um clique.", font=("Segoe UI", 10), fg='#b0b0b0', bg='#1a1a1a').pack()

        config_frame = tk.Frame(self, bg='#1a1a1a')
        config_frame.pack(fill='x', padx=20, pady=20)
        
        # Seções de configuração
        self._criar_secao_pasta(config_frame, "Pasta do Projeto", self.controller.pasta_selecionada, self.controller.selecionar_pasta_projeto, "Procurar...")
        self.label_saida, self.btn_procurar_saida = self._criar_secao_pasta(config_frame, "Arquivo de Saída", self.controller.caminho_saida, self.controller.selecionar_caminho_saida, "Salvar Como")
        self._criar_secao_opcoes(config_frame)
        
        self.btn_consolidar = tk.Button(self, text="CONSOLIDAR ARQUIVOS", command=self.controller.iniciar_processamento, bg='#4CAF50', fg='white', font=("Segoe UI", 12, "bold"), relief='flat', pady=10)
        self.btn_consolidar.pack(fill='x', padx=20, pady=10)

        # Log
        log_section = tk.Frame(self, bg='#1a1a1a')
        log_section.pack(fill='both', expand=True, padx=20, pady=5)
        tk.Label(log_section, text="Log de Processamento", font=("Segoe UI", 12, "bold"), fg="white", bg="#1a1a1a").pack(anchor='w')
        self.log_text = scrolledtext.ScrolledText(log_section, height=6, bg='#1e1e1e', fg='#00ff41', font=("Consolas", 9), relief='flat', insertbackground='white')
        self.log_text.pack(fill='both', expand=True, pady=(5,0))

        # Rodapé
        footer_frame = tk.Frame(self, bg='#1a1a1a')
        footer_frame.pack(fill='x', padx=20, pady=10)
        self.progress = ttk.Progressbar(footer_frame, mode='indeterminate')
        self.progress.pack(fill='x', pady=(0, 8))
        tk.Label(footer_frame, text="Desenvolvido por Comunidade DEV", font=("Segoe UI", 8, "italic"), fg='#888888', bg='#1a1a1a').pack()

    def _criar_secao_pasta(self, parent, label_text, text_variable, command, btn_text):
        section = tk.Frame(parent, bg='#2d2d2d')
        section.pack(fill='x', pady=(0, 6), ipady=10, ipadx=10)
        label = tk.Label(section, text=label_text, font=("Segoe UI", 12, "bold"), fg="white", bg="#2d2d2d")
        label.pack(anchor='w', padx=10, pady=(0, 5))
        
        input_frame = tk.Frame(section, bg="#2d2d2d")
        input_frame.pack(fill='x', padx=10)
        tk.Entry(input_frame, textvariable=text_variable, font=("Segoe UI", 10), bg='#404040', fg='white', relief='flat').pack(side='left', fill='x', expand=True, ipady=5)
        button = tk.Button(input_frame, text=btn_text, command=command, bg='#61dafb', fg='black', relief='flat')
        button.pack(side='right', padx=(8, 0))
        return label, button

    def _criar_secao_opcoes(self, parent):
        section = tk.Frame(parent, bg='#2d2d2d')
        section.pack(fill='x', pady=(0, 6), ipady=10, ipadx=10)
        tk.Label(section, text="Opções de Saída", font=("Segoe UI", 12, "bold"), fg="white", bg="#2d2d2d").pack(anchor='w', padx=10, pady=(0, 8))
        
        opcoes_frame = tk.Frame(section, bg="#2d2d2d")
        opcoes_frame.pack(fill='x', padx=10)
        style = ttk.Style()
        style.configure("TRadiobutton", background="#2d2d2d", foreground="white")
        ttk.Radiobutton(opcoes_frame, text="Arquivo Único", variable=self.controller.modo_saida, value="unique", command=self.controller.atualizar_interface_saida).pack(side='left', padx=(0, 20))
        ttk.Radiobutton(opcoes_frame, text="Arquivos Separados", variable=self.controller.modo_saida, value="split", command=self.controller.atualizar_interface_saida).pack(side='left')

    def log(self, message):
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)

    def clear_log(self):
        self.log_text.delete('1.0', tk.END)

    def set_progress(self, running):
        if running:
            self.progress.start(10)
            self.btn_consolidar.config(state='disabled', bg='#666')
        else:
            self.progress.stop()
            self.btn_consolidar.config(state='normal', bg='#4CAF50')
