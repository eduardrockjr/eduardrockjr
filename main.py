import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import socket
import time
from urllib.parse import urlparse

# ==========================================
# PALETA DE CORES (TEMA TELEGRAM DARK MODE)
# ==========================================
COR_FUNDO = "#17212b"          
COR_FUNDO_CAIXA = "#242f3d"    
COR_TEXTO = "#ffffff"          
COR_TELEGRAM_BLUE = "#5288c1"  
COR_BOTAO_PADRAO = "#2b5278"   
COR_BOTAO_HOVER = "#3e6a97"    
COR_TERMINAL = "#0e1621"       
COR_TEXTO_TERM = "#ffffff"

def obter_url():
    url = entry_url.get().strip()
    if not url:
        messagebox.showwarning("Aviso", "Por favor, digite a URL do alvo.")
        return None
    if url.startswith("http://"): url = url[7:]
    if url.startswith("https://"): url = url[8:]
    return url

def obter_dominio_puro():
    url = obter_url()
    if not url: return None
    return url.split('/')[0]

# ==========================================
# MÓDULOS DE RECONHECIMENTO (FUNÇÕES)
# ==========================================

def testar_clickjacking():
    dom = obter_dominio_puro()
    if not dom: return
    txt_resultado.insert(tk.END, f"[*] Testando Clickjacking em: https://{dom}\n{'-'*60}\n")
    janela.update()
    try:
        resposta = requests.get(f"https://{dom}", timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        cabes = resposta.headers
        if 'X-Frame-Options' not in cabes and 'Content-Security-Policy' not in cabes:
            txt_resultado.insert(tk.END, "[ VULNERÁVEL ] Faltam proteções (X-Frame-Options e CSP ausentes).\n\n", 'perigo')
        else:
            txt_resultado.insert(tk.END, "[ SEGURO ] Proteção contra Clickjacking detectada.\n\n", 'seguro')
    except requests.exceptions.RequestException as e:
        txt_resultado.insert(tk.END, f"[ ERRO ] Falha na conexão: {e}\n\n", 'perigo')

def testar_cookies():
    dom = obter_dominio_puro()
    if not dom: return
    txt_resultado.insert(tk.END, f"[*] Testando Flags de Cookies em: https://{dom}\n{'-'*60}\n")
    janela.update()
    try:
        resposta = requests.get(f"https://{dom}", timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        cabes = resposta.headers
        if 'Set-Cookie' in cabes:
            cookie_info = cabes['Set-Cookie']
            if 'Secure' not in cookie_info or 'HttpOnly' not in cookie_info:
                txt_resultado.insert(tk.END, f"[ ALERTA ] Cookies configurados sem as diretrizes ideais de segurança.\n\n", 'alerta')
            else:
                txt_resultado.insert(tk.END, "[ OK ] Cookies utilizando flags de segurança corretamente.\n\n", 'seguro')
        else:
            txt_resultado.insert(tk.END, "[ INFO ] Nenhum cookie foi gerado na resposta inicial.\n\n", 'info')
    except requests.exceptions.RequestException as e:
        txt_resultado.insert(tk.END, f"[ ERRO ] Falha na conexão: {e}\n\n", 'perigo')

def testar_hsts_e_headers():
    dom = obter_dominio_puro()
    if not dom: return
    txt_resultado.insert(tk.END, f"[*] Analisando Cabeçalhos de Segurança em: https://{dom}\n{'-'*60}\n")
    janela.update()
    try:
        resposta = requests.get(f"https://{dom}", timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        headers = resposta.headers
        
        if 'Strict-Transport-Security' in headers:
            txt_resultado.insert(tk.END, "[ OK ] Cabeçalho HSTS ativo (Força HTTPS).\n", 'seguro')
        else:
            txt_resultado.insert(tk.END, "[ VULNERÁVEL ] Cabeçalho HSTS ausente.\n", 'perigo')
            
        if 'X-Content-Type-Options' in headers:
            txt_resultado.insert(tk.END, "[ OK ] X-Content-Type-Options configurado (Proteção MIME).\n", 'seguro')
        else:
            txt_resultado.insert(tk.END, "[ ALERTA ] X-Content-Type-Options ausente.\n", 'alerta')
            
        txt_resultado.insert(tk.END, "\n")
    except requests.exceptions.RequestException as e:
        txt_resultado.insert(tk.END, f"[ ERRO ] Falha na conexão: {e}\n\n", 'perigo')

def testar_server_info():
    dom = obter_dominio_puro()
    if not dom: return
    txt_resultado.insert(tk.END, f"[*] Analisando Infraestrutura de Rede: {dom}\n{'-'*60}\n")
    janela.update()
    try:
        resposta = requests.get(f"https://{dom}", timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        servidor = resposta.headers.get('Server', 'Oculto / Protegido')
        tecnologia = resposta.headers.get('X-Powered-By', 'Oculto / Não revelado')
        txt_resultado.insert(tk.END, f"[ INFO ] Servidor visível: {servidor}\n", 'info')
        txt_resultado.insert(tk.END, f"[ INFO ] Backend tecnológico: {tecnologia}\n", 'info')
        
        ip_alvo = socket.gethostbyname(dom)
        txt_resultado.insert(tk.END, f"[ INFO ] Endereço IP do Host: {ip_alvo}\n\n", 'seguro')
    except Exception as e:
        txt_resultado.insert(tk.END, f"[ ERRO ] Falha ao coletar dados de rede: {e}\n\n", 'perigo')

def verificar_robots():
    dom = obter_dominio_puro()
    if not dom: return
    
    # MUDA O TEXTO DO BOTÃO ASSIM QUE A FUNÇÃO É CHAMADA
    btn_robots.config(text="🤖 Ler robots.txt")
    
    robots_url = f"https://{dom}/robots.txt"
    txt_resultado.insert(tk.END, f"[*] Lendo arquivo de mapeamento: {robots_url}\n{'-'*60}\n")
    janela.update()
    try:
        cabecalhos = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        resposta = requests.get(robots_url, headers=cabecalhos, timeout=5)
        
        if resposta.status_code == 200:
            txt_resultado.insert(tk.END, "[ ENCONTRADO ] robots.txt público. Primeiras linhas identificadas:\n", 'alerta')
            linhas = resposta.text.split('\n')[:5]
            for linha in linhas:
                txt_resultado.insert(tk.END, f"   > {linha}\n", 'info')
            txt_resultado.insert(tk.END, "\n")
        elif resposta.status_code == 403:
            txt_resultado.insert(tk.END, "[ BLOQUEADO ] O Firewall de Aplicação (WAF) barrou a leitura (403).\n\n", 'perigo')
        else:
            txt_resultado.insert(tk.END, f"[ INFO ] Arquivo inexistente no servidor público (Status {resposta.status_code}).\n\n", 'info')
    except requests.exceptions.RequestException as e:
        txt_resultado.insert(tk.END, f"[ ERRO ] Erro de comunicação: {e}\n\n", 'perigo')

def explorar_robots_auto():
    dom = obter_dominio_puro()
    if not dom: return
    robots_url = f"https://{dom}/robots.txt"
    txt_resultado.insert(tk.END, f"[*] Mapeando rotas restritas via robots.txt...\n{'-'*60}\n")
    janela.update()
    try:
        cabecalhos = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        resposta = requests.get(robots_url, headers=cabecalhos, timeout=5)
        if resposta.status_code != 200:
            txt_resultado.insert(tk.END, f"[ ERRO ] Não foi possível extrair parâmetros (Status {resposta.status_code}).\n\n", 'perigo')
            return

        caminhos = []
        for linha in resposta.text.split('\n'):
            if 'Disallow:' in linha:
                partes = linha.split('Disallow:')
                if len(partes) > 1:
                    limpo = partes[1].strip().replace('*', '')
                    if limpo.startswith('/'):
                        caminhos.append(limpo)
        caminhos = list(set(caminhos))
        
        if not caminhos:
            txt_resultado.insert(tk.END, "[ INFO ] Nenhuma rota oculta declarada no arquivo.\n\n", 'info')
            return
            
        txt_resultado.insert(tk.END, f"[+] Identificados {len(caminhos)} caminhos restritos. Analisando permissões...\n", 'info')
        janela.update()
        
        for caminho in caminhos[:12]:
            url_teste = f"https://{dom}" + caminho
            try:
                req = requests.get(url_teste, headers=cabecalhos, timeout=3)
                if req.status_code == 200:
                    txt_resultado.insert(tk.END, f"[ 200 OK ] ACESSO ABERTO! -> {url_teste}\n", 'seguro')
                elif req.status_code in [401, 403]:
                    txt_resultado.insert(tk.END, f"[ {req.status_code} ] Protegido -> {caminho}\n", 'alerta')
                else:
                    txt_resultado.insert(tk.END, f"[ {req.status_code} ] Retorno padrão -> {caminho}\n", 'info')
            except requests.exceptions.RequestException:
                 txt_resultado.insert(tk.END, f"[ ERRO ] Instabilidade/Timeout -> {caminho}\n", 'perigo')
            time.sleep(0.4)
            janela.update()
        txt_resultado.insert(tk.END, "\n[ OK ] Mapeamento de rotas concluído.\n\n", 'info')
    except Exception as e:
        txt_resultado.insert(tk.END, f"[ ERRO ] Falha geral na execução do módulo: {e}\n\n", 'perigo')

def buscar_subdominios_osint():
    dom = obter_dominio_puro()
    if not dom: return
    txt_resultado.insert(tk.END, f"[*] Buscando subdomínios via Certificados Digitais (OSINT Passivo): {dom}\n{'-'*60}\n")
    txt_resultado.insert(tk.END, "Consultando base de dados crt.sh (pode levar alguns segundos)...\n", 'info')
    janela.update()
    
    try:
        url_api = f"https://crt.sh/?q=%.{dom}&output=json"
        resposta = requests.get(url_api, timeout=15)
        
        if resposta.status_code == 200:
            dados = resposta.json()
            subdominios = set()
            
            for item in dados:
                nome = item['name_value'].lower()
                for sub in nome.split('\n'):
                    sub = sub.strip().replace('*.', '')
                    if sub.endswith(dom) and sub != dom:
                        subdominios.add(sub)
            
            lista_ordenada = sorted(list(subdominios))
            
            if not lista_ordenada:
                txt_resultado.insert(tk.END, "[ INFO ] Nenhum subdomínio alternativo mapeado nos certificados recentes.\n\n", 'info')
            else:
                txt_resultado.insert(tk.END, f"[+] Sucesso! Encontrados {len(lista_ordenada)} subdomínios mapeados:\n", 'seguro')
                for s in lista_ordenada[:20]:
                    txt_resultado.insert(tk.END, f"   > {s}\n", 'info')
                if len(lista_ordenada) > 20:
                    txt_resultado.insert(tk.END, f"   ... e mais {len(lista_ordenada)-20} subdomínios listados na base.\n", 'alerta')
                txt_resultado.insert(tk.END, "\n")
        else:
            txt_resultado.insert(tk.END, f"[ ERRO ] Base crt.sh retornou código inválido: {resposta.status_code}\n\n", 'perigo')
    except Exception as e:
        txt_resultado.insert(tk.END, f"[ ERRO ] Falha de timeout ou leitura na API OSINT: {e}\n\n", 'perigo')

def limpar_tela():
    entry_url.delete(0, tk.END)
    txt_resultado.delete(1.0, tk.END)
    # Reseta o botão do robots para o estado original também
    btn_robots.config(text="📄 Criar robots.txt")

# ==========================================
# CONFIGURAÇÃO INTERFACE GRÁFICA (TELEGRAM)
# ==========================================
janela = tk.Tk()
janela.title("Canivete Suíço de Reconhecimento - Telegram Edition")
janela.geometry("800x650")
janela.configure(bg=COR_FUNDO)

# --- CABEÇALHO ---
frame_header = tk.Frame(janela, bg=COR_TELEGRAM_BLUE, height=55)
frame_header.pack(fill="x", side="top")
frame_header.pack_propagate(False)

# TEXTO ALTERADO AQUI
lbl_titulo = tk.Label(frame_header, text="Canivete Suíço - by edyerockjr", bg=COR_TELEGRAM_BLUE, fg=COR_TEXTO, font=("Arial", 13, "bold"))
lbl_titulo.pack(side="left", padx=20, pady=15)

# --- CORPO ---
frame_corpo = tk.Frame(janela, bg=COR_FUNDO)
frame_corpo.pack(fill="both", expand=True, padx=25, pady=15)

lbl_url = tk.Label(frame_corpo, text="Domínio ou URL Alvo:", bg=COR_FUNDO, fg=COR_TEXTO, font=("Arial", 11, "bold"))
lbl_url.pack(anchor="w", pady=(0, 5))

entry_url = tk.Entry(frame_corpo, width=85, font=("Arial", 11), bg=COR_FUNDO_CAIXA, fg=COR_TEXTO, insertbackground=COR_TEXTO, relief="flat")
entry_url.pack(ipady=7, fill="x")
entry_url.insert(0, "site-de-teste.com.br")

# --- CONTEINER DE BOTÕES ---
frame_botoes = tk.Frame(frame_corpo, bg=COR_FUNDO)
frame_botoes.pack(pady=15, fill="x")

estilo_btn = {
    "bg": COR_BOTAO_PADRAO, "fg": COR_TEXTO, "font": ("Arial", 10, "bold"),
    "activebackground": COR_BOTAO_HOVER, "activeforeground": COR_TEXTO,
    "relief": "flat", "height": 2, "cursor": "hand2"
}

tk.Button(frame_botoes, text="🔍 Clickjacking", command=testar_clickjacking, **estilo_btn).grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
tk.Button(frame_botoes, text="🍪 Cookies Check", command=testar_cookies, **estilo_btn).grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
tk.Button(frame_botoes, text="🔒 HSTS & Headers", command=testar_hsts_e_headers, **estilo_btn).grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

tk.Button(frame_botoes, text="🖥️ Servidor & IP", command=testar_server_info, **estilo_btn).grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

# BOTÃO ROBOTS ISOLADO PARA PODER MUDAR O TEXTO
btn_robots = tk.Button(frame_botoes, text="📄 Criar robots.txt", command=verificar_robots, **estilo_btn)
btn_robots.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

tk.Button(frame_botoes, text="⚡ Explorar Rotas", command=explorar_robots_auto, **estilo_btn).grid(row=1, column=2, padx=5, pady=5, sticky="nsew")

tk.Button(frame_botoes, text="🌐 Mapear Subdomínios", command=buscar_subdominios_osint, bg="#2f6ea7", fg=COR_TEXTO, font=("Arial", 10, "bold"), activebackground=COR_TELEGRAM_BLUE, relief="flat", height=2, cursor="hand2").grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

tk.Button(frame_botoes, text="🗑️ Limpar Saída", command=limpar_tela, bg="#9e3a3a", fg=COR_TEXTO, font=("Arial", 10, "bold"), activebackground="#bd4f4f", relief="flat", height=2, cursor="hand2").grid(row=2, column=2, padx=5, pady=5, sticky="nsew")

frame_botoes.grid_columnconfigure(0, weight=1)
frame_botoes.grid_columnconfigure(1, weight=1)
frame_botoes.grid_columnconfigure(2, weight=1)

# --- TERMINAL ---
lbl_resultado = tk.Label(frame_corpo, text="Resultado da Varredura:", bg=COR_FUNDO, fg=COR_TEXTO, font=("Arial", 11, "bold"))
lbl_resultado.pack(anchor="w", pady=(5, 2))

txt_resultado = scrolledtext.ScrolledText(frame_corpo, font=("Consolas", 10), bg=COR_TERMINAL, fg=COR_TEXTO_TERM, relief="flat")
txt_resultado.pack(fill="both", expand=True, pady=5)

txt_resultado.tag_config('perigo', foreground='#ff5252') 
txt_resultado.tag_config('alerta', foreground='#ffca28') 
txt_resultado.tag_config('seguro', foreground='#43a047') 
txt_resultado.tag_config('info', foreground='#64b5f6')   

janela.mainloop()