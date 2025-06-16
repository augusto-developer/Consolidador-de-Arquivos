import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from pathlib import Path

# Importa os componentes da GUI e a lógica de negócio
from .painel_lateral import PainelLateral
from .painel_principal import PainelPrincipal
from services.cp_service import listar_arquivos_python, processar_arquivos

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Consolidador Python (Refatorado)")
        self.geometry("900x600")
        self.resizable(False, False)
        self.configure(bg='#1a1a1a')

        # Variáveis de estado da aplicação
        self.pasta_selecionada = tk.StringVar()
        self.caminho_saida = tk.StringVar(value=str(Path.home() / "Desktop" / "codigo_consolidado.txt"))
        self.modo_saida = tk.StringVar(value="unique")

        self._criar_widgets()

    def _criar_widgets(self):
        """Cria e organiza os componentes principais da interface."""
        main_container = tk.Frame(self, bg='#1a1a1a')
        main_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Instancia os painéis, passando a si mesma como controladora
        self.painel_lateral = PainelLateral(main_container, self)
        tk.Frame(main_container, bg='#404040', width=2).pack(side='left', fill='y', padx=8)
        self.painel_principal = PainelPrincipal(main_container, self)

    def selecionar_pasta_projeto(self):
        """Abre o diálogo para selecionar a pasta do projeto e carrega os arquivos."""
        pasta = filedialog.askdirectory(title="Selecione a pasta do projeto")
        if not pasta: return
        
        self.pasta_selecionada.set(pasta)
        self.painel_principal.clear_log()
        self.painel_principal.log(f"Buscando arquivos em: {pasta}\n")
        
        arquivos = listar_arquivos_python(pasta)
        self.painel_lateral.carregar_arquivos(arquivos)
        self.painel_principal.log(f"Encontrados {len(arquivos)} arquivos Python.\n")

    def selecionar_caminho_saida(self):
        """Abre o diálogo para selecionar o arquivo ou pasta de saída."""
        modo = self.modo_saida.get()
        if modo == "unique":
            path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], title="Salvar Arquivo Consolidado")
        else:
            path = filedialog.askdirectory(title="Selecione a Pasta de Saída")
        
        if path:
            self.caminho_saida.set(path)

    def atualizar_interface_saida(self):
        """Ajusta a interface do painel principal com base na opção de saída."""
        modo = self.modo_saida.get()
        if modo == "unique":
            self.painel_principal.label_saida.config(text="Arquivo de Saída")
            self.painel_principal.btn_procurar_saida.config(text="Salvar Como")
        else:
            self.painel_principal.label_saida.config(text="Pasta de Saída")
            self.painel_principal.btn_procurar_saida.config(text="Selecionar Pasta...")

    def iniciar_processamento(self):
        """Valida as entradas e inicia o processamento em uma nova thread."""
        arquivos = self.painel_lateral.obter_arquivos_selecionados()
        if not arquivos:
            messagebox.showwarning("Atenção", "Selecione ao menos um arquivo para processar.")
            return

        caminho = self.caminho_saida.get()
        if not caminho:
            messagebox.showwarning("Atenção", "Defina um caminho de saída.")
            return

        # Atualiza a UI para o estado de "processando"
        self.painel_principal.set_progress(True)
        
        # Cria e inicia a thread para não travar a interface
        thread = threading.Thread(target=self._executar_processamento, args=(arquivos, caminho, self.modo_saida.get()))
        thread.daemon = True
        thread.start()

    def _executar_processamento(self, arquivos, caminho, modo):
        """
        Método executado na thread. Chama a lógica de negócio e atualiza a UI no final.
        """
        painel = self.painel_principal
        painel.clear_log()
        painel.log(f"Iniciando no modo: '{'Arquivo Único' if modo == 'unique' else 'Arquivos Separados'}'\n")
        
        try:
            # === ESTA É A CHAMADA CORRETA PARA A LÓGICA ===
            total = processar_arquivos(arquivos, caminho, modo)
            
            painel.log(f"Sucesso! {total} arquivos foram processados.\n")
            messagebox.showinfo("Processamento Concluído", f"{total} arquivos processados com sucesso!")
        except Exception as e:
            painel.log(f"ERRO: {e}\n")
            messagebox.showerror("Erro no Processamento", f"Ocorreu um erro inesperado:\n{e}")
        finally:
            # Garante que a UI volte ao normal, mesmo se ocorrer um erro
            painel.set_progress(False)

    def run(self):
        """Inicia o loop principal da aplicação."""
        self.mainloop()
