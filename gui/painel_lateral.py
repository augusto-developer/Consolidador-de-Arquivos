import tkinter as tk
from tkinter import ttk

class PainelLateral(tk.Frame):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, bg='#2d2d2d', width=320, **kwargs)
        self.controller = controller  # Referência ao controlador principal

        self.pack(side='left', fill='y')
        self.pack_propagate(False)
        
        self.checkboxes_arquivos = {}
        self._criar_widgets()

    def _on_mousewheel(self, event):
        self.canvas_arquivos.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _criar_widgets(self):
        # Cabeçalho
        tk.Label(self, text="Arquivos Python Encontrados", font=("Segoe UI", 13, "bold"), fg='#61dafb', bg='#2d2d2d').pack(pady=(18, 10))

        # Botões Marcar/Desmarcar
        botoes_frame = tk.Frame(self, bg='#2d2d2d')
        botoes_frame.pack(fill='x', padx=15, pady=8)
        tk.Button(botoes_frame, text="Marcar Todos", command=self.selecionar_todos, bg='#4CAF50', fg='white', relief='flat').pack(side='left', expand=True, fill='x', padx=(0, 4))
        tk.Button(botoes_frame, text="Desmarcar Todos", command=self.desmarcar_todos, bg='#f44336', fg='white', relief='flat').pack(side='right', expand=True, fill='x', padx=(4, 0))

        # Lista de arquivos com scroll
        scroll_container = tk.Frame(self, bg='#1e1e1e')
        scroll_container.pack(fill='both', expand=True, padx=15, pady=5)
        self.canvas_arquivos = tk.Canvas(scroll_container, bg='#1e1e1e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=self.canvas_arquivos.yview)
        self.frame_arquivos = tk.Frame(self.canvas_arquivos, bg='#1e1e1e')
        
        self.canvas_arquivos.configure(yscrollcommand=scrollbar.set)
        self.canvas_arquivos.create_window((0, 0), window=self.frame_arquivos, anchor="nw")
        self.frame_arquivos.bind("<Configure>", lambda e: self.canvas_arquivos.configure(scrollregion=self.canvas_arquivos.bbox("all")))
        
        self.canvas_arquivos.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.canvas_arquivos.bind_all("<MouseWheel>", self._on_mousewheel)

        # Contador
        self.label_contador = tk.Label(self, text="Nenhum arquivo encontrado", font=("Segoe UI", 10, "bold"), fg='#61dafb', bg='#2d2d2d')
        self.label_contador.pack(pady=10)

    def carregar_arquivos(self, arquivos_encontrados):
        for widget in self.frame_arquivos.winfo_children():
            widget.destroy()
        self.checkboxes_arquivos.clear()

        for i, arquivoinfo in enumerate(arquivos_encontrados):
            var = tk.BooleanVar(value=True)
            check_frame = tk.Frame(self.frame_arquivos, bg='#1e1e1e')
            check = tk.Checkbutton(check_frame, text=str(arquivoinfo['caminhorelativo']), variable=var, 
                                   bg='#1e1e1e', fg='white', selectcolor='#404040', relief='flat', 
                                   anchor='w', command=self.atualizar_contador)
            check.pack(fill='x', expand=True)
            check_frame.pack(fill='x', expand=True, padx=5, pady=2)
            check.bind("<MouseWheel>", self._on_mousewheel)
            self.checkboxes_arquivos[i] = {'var': var, 'arquivoinfo': arquivoinfo}
        
        self.atualizar_contador()

    def atualizar_contador(self):
        selecionados = sum(1 for data in self.checkboxes_arquivos.values() if data['var'].get())
        total = len(self.checkboxes_arquivos)
        self.label_contador.config(text=f"{selecionados} de {total} selecionados")
        
    def selecionar_todos(self):
        for data in self.checkboxes_arquivos.values(): data['var'].set(True)
        self.atualizar_contador()

    def desmarcar_todos(self):
        for data in self.checkboxes_arquivos.values(): data['var'].set(False)
        self.atualizar_contador()

    def obter_arquivos_selecionados(self):
        return [data['arquivoinfo'] for data in self.checkboxes_arquivos.values() if data['var'].get()]
