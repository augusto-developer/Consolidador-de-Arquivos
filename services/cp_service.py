import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
from pathlib import Path

# ========== LÓGICA DE CONSOLIDAÇÃO ==========

PASTAS_IGNORADAS = {'.venv', 'venv', '.env', 'env', '__pycache__', '.git', 'node_modules', '.pytest_cache', 'build', 'dist', '.idea', '.vscode'}

def listar_arquivos_python(pasta_projeto):
    pasta_projeto = Path(pasta_projeto)
    arquivos_encontrados = []
    for arquivo_py in pasta_projeto.rglob('*.py'):
        try:
            if any(parte in PASTAS_IGNORADAS for parte in arquivo_py.parts):
                continue
            caminho_relativo = arquivo_py.relative_to(pasta_projeto)
            arquivos_encontrados.append({
                'caminhocompleto': arquivo_py,
                'caminhorelativo': caminho_relativo,
                'nome': arquivo_py.name
            })
        except Exception:
            continue
    return sorted(arquivos_encontrados, key=lambda x: x['nome'])

def salvar_arquivo_unico(arquivos_selecionados, arquivo_saida):
    conteudo_consolidado = []
    arquivos_processados = 0
    for arquivoinfo in arquivos_selecionados:
        try:
            with open(arquivoinfo['caminhocompleto'], 'r', encoding='utf-8') as file:
                conteudo = file.read()
            conteudo_consolidado.append(f"# Arquivo: {arquivoinfo['caminhorelativo']}\n\n")
            conteudo_consolidado.append(f"{conteudo}\n\n")
            conteudo_consolidado.append("-" * 80 + "\n\n")
            arquivos_processados += 1
        except Exception:
            continue
    with open(arquivo_saida, 'w', encoding='utf-8') as file:
        file.writelines(conteudo_consolidado)
    return arquivos_processados

def salvar_arquivos_separados(arquivos_selecionados, pasta_saida):
    output_dir = Path(pasta_saida)
    output_dir.mkdir(parents=True, exist_ok=True)
    arquivos_processados = 0
    for arquivoinfo in arquivos_selecionados:
        try:
            caminho_completo = arquivoinfo['caminhocompleto']
            nome_arquivo_original = arquivoinfo['nome']
            caminho_destino = output_dir / f"{nome_arquivo_original}.txt"
            with open(caminho_completo, 'r', encoding='utf-8') as f_in:
                conteudo = f_in.read()
            with open(caminho_destino, 'w', encoding='utf-8') as f_out:
                f_out.write(f"# Arquivo Original: {arquivoinfo['caminhorelativo']}\n\n")
                f_out.write(conteudo)
            arquivos_processados += 1
        except Exception:
            continue
    return arquivos_processados

def processar_arquivos(arquivos_selecionados, caminho_saida, modo):
    if modo == "unique":
        return salvar_arquivo_unico(arquivos_selecionados, caminho_saida)
    elif modo == "split":
        return salvar_arquivos_separados(arquivos_selecionados, caminho_saida)
    else:
        raise ValueError("Modo inválido.")