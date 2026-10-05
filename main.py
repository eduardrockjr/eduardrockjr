import customtkinter as ctk
import asyncio
import threading
import os
import webbrowser
from tkinter import filedialog
from telethon import TelegramClient

# Configuração visual do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppTelegram(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Variáveis de controle de segurança e estado
        self.phone_code_hash = None
        self.is_paused = False
        self.is_running = False
        self.pasta_destino = os.path.abspath("arquivos_baixados")

        # --- CONFIGURAÇÃO DA JANELA PRINCIPAL ---
        self.title("Módulo de Imersão - Extrator de Dados do Telegram")
        # Janela mais larga e menos alta para acomodar os botões lado a lado
        self.geometry("820x620") 
        self.resizable(True, True) 

        self.titulo = ctk.CTkLabel(self, text="Extrator de Mídia e Mensagens", font=("Roboto", 22, "bold"))
        self.titulo.pack(pady=15)

        # ==========================================
        # SISTEMA DE ABAS (WIZARD DE ETAPAS)
        # ==========================================
        self.abas = ctk.CTkTabview(self, width=760, height=340)
        self.abas.pack(pady=5, padx=20)

        self.abas.add("Passo 1: Criar API")
        self.abas.add("Passo 2: Credenciais")
        self.abas.add("Passo 3: Salvar e Extrair")

        self.montar_passo_1()
        self.montar_passo_2()
        self.montar_passo_3()

        # --- ÁREA DE LOGS FIXA ---
        self.txt_logs = ctk.CTkTextbox(self, width=760, height=160, font=("Consolas", 12))
        self.txt_logs.pack(pady=15, padx=20)
        self.escrever_log("Sistema inicializado. Interface otimizada carregada com sucesso!")

    def escrever_log(self, texto):
        self.txt_logs.insert("end", f"{texto}\n")
        self.txt_logs.see("end")

    # ==========================================
    # INTERFACE: PASSO 1
    # ==========================================
    def montar_passo_1(self):
        aba = self.abas.tab("Passo 1: Criar API")
        
        texto_instrucoes = (
            "Siga os passos abaixo para obter suas credenciais gratuitas do Telegram:\n\n"
            "1. Clique no botão abaixo para abrir o portal oficial.\n"
            "2. Faça login com seu número de telefone (+55 DDD Número).\n"
            "3. Vá em 'API development tools' e crie um novo aplicativo.\n"
            "4. Salve o 'App api_id' e o 'App api_hash'.\n"
            "5. Avance para o Passo 2 para configurar o sistema."
        )
        
        lbl_instrucoes = ctk.CTkLabel(aba, text=texto_instrucoes, font=("Roboto", 14), justify="left")
        lbl_instrucoes.pack(pady=15)

        btn_site = ctk.CTkButton(aba, text="Abrir Portal do Telegram", font=("Roboto", 14, "bold"), height=40, width=250, 
                                 command=lambda: webbrowser.open("https://my.telegram.org/"))
        btn_site.pack(pady=10)

        btn_avancar = ctk.CTkButton(aba, text="Já tenho os dados ➔", font=("Roboto", 12, "bold"), fg_color="#27AE60", hover_color="#2ECC71", width=200,
                                    command=lambda: self.abas.set("Passo 2: Credenciais"))
        btn_avancar.pack(pady=10)

    # ==========================================
    # INTERFACE: PASSO 2
    # ==========================================
    def montar_passo_2(self):
        aba = self.abas.tab("Passo 2: Credenciais")

        frame_grid = ctk.CTkFrame(aba, fg_color="transparent")
        frame_grid.pack(pady=10)

        ctk.CTkLabel(frame_grid, text="API ID:").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.txt_api_id = ctk.CTkEntry(frame_grid, placeholder_text="Ex: 1234567", width=160)
        self.txt_api_id.grid(row=0, column=1, padx=5, pady=8)

        ctk.CTkLabel(frame_grid, text="API Hash:").grid(row=0, column=2, padx=10, pady=8, sticky="w")
        self.txt_api_hash = ctk.CTkEntry(frame_grid, placeholder_text="Ex: abcdef123...", width=200)
        self.txt_api_hash.grid(row=0, column=3, padx=5, pady=8)

        ctk.CTkLabel(frame_grid, text="Telefone:").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        self.txt_phone = ctk.CTkEntry(frame_grid, placeholder_text="+55...", width=160)
        self.txt_phone.grid(row=1, column=1, padx=5, pady=8)

        ctk.CTkLabel(frame_grid, text="Grupo/Canal:").grid(row=1, column=2, padx=10, pady=8, sticky="w")
        self.txt_grupo = ctk.CTkEntry(frame_grid, placeholder_text="@grupo ou link", width=200)
        self.txt_grupo.grid(row=1, column=3, padx=5, pady=8)

        ctk.CTkLabel(frame_grid, text="Cód. Verificação:").grid(row=2, column=0, padx=10, pady=8, sticky="w")
        self.txt_codigo = ctk.CTkEntry(frame_grid, placeholder_text="5 dígitos", width=160)
        self.txt_codigo.grid(row=2, column=1, padx=5, pady=8)

        self.btn_solicitar = ctk.CTkButton(frame_grid, text="Solicitar Código", command=self.disparar_codigo, fg_color="#E67E22", hover_color="#D35400", width=140)
        self.btn_solicitar.grid(row=2, column=2, columnspan=2, padx=10, pady=8, sticky="w")

        frame_nav = ctk.CTkFrame(aba, fg_color="transparent")
        frame_nav.pack(pady=15)

        btn_voltar = ctk.CTkButton(frame_nav, text="⇠ Voltar Instruções", font=("Roboto", 12), fg_color="#5D6D7E", width=180,
                                   command=lambda: self.abas.set("Passo 1: Criar API"))
        btn_voltar.grid(row=0, column=0, padx=10)

        btn_avancar = ctk.CTkButton(frame_nav, text="Próximo Passo ➔", font=("Roboto", 12, "bold"), fg_color="#27AE60", hover_color="#2ECC71", width=180,
                                    command=lambda: self.abas.set("Passo 3: Salvar e Extrair"))
        btn_avancar.grid(row=0, column=1, padx=10)

    # ==========================================
    # INTERFACE: PASSO 3 (BOTÕES LADO A LADO)
    # ==========================================
    def montar_passo_3(self):
        aba = self.abas.tab("Passo 3: Salvar e Extrair")

        frame_pasta = ctk.CTkFrame(aba, fg_color="transparent")
        frame_pasta.pack(pady=15)

        ctk.CTkLabel(frame_pasta, text="Caminho de Salvamento:", font=("Roboto", 14)).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        self.txt_pasta = ctk.CTkEntry(frame_pasta, width=480)
        self.txt_pasta.insert(0, self.pasta_destino)
        self.txt_pasta.grid(row=1, column=0, padx=10, pady=5)

        self.btn_escolher_pasta = ctk.CTkButton(frame_pasta, text="Escolher Pasta", command=self.abrir_janela_pastas, width=120)
        self.btn_escolher_pasta.grid(row=1, column=1, padx=10, pady=5)

        # --- NOVA GRADE HORIZONTAL PARA OS BOTÕES ---
        frame_acao = ctk.CTkFrame(aba, fg_color="transparent")
        frame_acao.pack(pady=15)

        # Botão Fotos
        self.btn_fotos = ctk.CTkButton(frame_acao, text="📸 Fotos", command=lambda: self.disparar_extracao("fotos"), font=("Roboto", 13, "bold"), height=40, width=150, fg_color="#2980B9", hover_color="#3498DB")
        self.btn_fotos.grid(row=0, column=0, padx=8)

        # Botão Vídeos
        self.btn_videos = ctk.CTkButton(frame_acao, text="🎬 Vídeos", command=lambda: self.disparar_extracao("videos"), font=("Roboto", 13, "bold"), height=40, width=150, fg_color="#8E44AD", hover_color="#9B59B6")
        self.btn_videos.grid(row=0, column=1, padx=8)

        # Botão Ambos
        self.btn_ambos = ctk.CTkButton(frame_acao, text="🌟 Ambos", command=lambda: self.disparar_extracao("ambos"), font=("Roboto", 13, "bold"), height=40, width=150, fg_color="#27AE60", hover_color="#2ECC71")
        self.btn_ambos.grid(row=0, column=2, padx=8)

        # Botão Pausar / Continuar
        self.btn_pausar = ctk.CTkButton(frame_acao, text="Pausar", command=self.alternar_pausa, font=("Roboto", 13, "bold"), height=40, width=150, state="disabled", fg_color="#7F8C8D")
        self.btn_pausar.grid(row=0, column=3, padx=8)

        # Voltar
        btn_voltar_cred = ctk.CTkButton(aba, text="⇠ Voltar para Credenciais", font=("Roboto", 12), fg_color="#5D6D7E", width=220,
                                        command=lambda: self.abas.set("Passo 2: Credenciais"))
        btn_voltar_cred.pack(pady=10)

    # ==========================================
    # FUNÇÕES DE LÓGICA INTERNA
    # ==========================================
    def abrir_janela_pastas(self):
        pasta_selecionada = filedialog.askdirectory(initialdir=self.pasta_destino, title="Selecione a pasta de destino")
        if pasta_selecionada:
            self.pasta_destino = os.path.abspath(pasta_selecionada)
            self.txt_pasta.delete(0, "end")
            self.txt_pasta.insert(0, self.pasta_destino)
            self.escrever_log(f"[CONFIG] Destino: {self.pasta_destino}")

    def alternar_pausa(self):
        if not self.is_running: return
        if self.is_paused:
            self.is_paused = False
            self.btn_pausar.configure(text="Pausar", fg_color="#E67E22")
            self.escrever_log("[AVISO] Extração retomada!")
        else:
            self.is_paused = True
            self.btn_pausar.configure(text="Continuar", fg_color="#27AE60")
            self.escrever_log("[AVISO] Extração PAUSADA!")

    def disparar_codigo(self): threading.Thread(target=self.executar_codigo_async, daemon=True).start()
    def executar_codigo_async(self):
        loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop)
        loop.run_until_complete(self.processo_pedir_codigo()); loop.close()

    async def processo_pedir_codigo(self):
        api_id, api_hash, phone = self.txt_api_id.get().strip(), self.txt_api_hash.get().strip(), self.txt_phone.get().strip()
        if not api_id or not api_hash or not phone:
            self.escrever_log("[ERRO] Preencha os campos na Aba 2."); return
        self.btn_solicitar.configure(state="disabled")
        client = TelegramClient('sessao_trabalho', int(api_id), api_hash)
        try:
            await client.connect()
            if not await client.is_user_authorized():
                resultado = await client.send_code_request(phone)
                self.phone_code_hash = resultado.phone_code_hash
                self.escrever_log("[SUCESSO] Código enviado! Verifique seu app.")
            else: self.escrever_log("[AVISO] Já logado!")
        except Exception as e: self.escrever_log(f"[ERRO] {str(e)}")
        finally: await client.disconnect(); self.btn_solicitar.configure(state="normal")

    def disparar_extracao(self, tipo_midia): 
        threading.Thread(target=self.executar_loop_async, args=(tipo_midia,), daemon=True).start()

    def executar_loop_async(self, tipo_midia):
        loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop)
        loop.run_until_complete(self.processo_extracao(tipo_midia)); loop.close()

    async def processo_extracao(self, tipo_midia):
        api_id, api_hash, phone = self.txt_api_id.get().strip(), self.txt_api_hash.get().strip(), self.txt_phone.get().strip()
        grupo_alvo, cod, dest = self.txt_grupo.get().strip(), self.txt_codigo.get().strip(), self.txt_pasta.get().strip()
        if not api_id or not api_hash or not phone or not grupo_alvo or not dest:
            self.escrever_log("[ERRO] Preencha tudo nas Abas 2 e 3."); return
        
        self.btn_fotos.configure(state="disabled")
        self.btn_videos.configure(state="disabled")
        self.btn_ambos.configure(state="disabled")
        self.btn_escolher_pasta.configure(state="disabled")
        
        self.is_running, self.is_paused = True, False
        self.btn_pausar.configure(state="normal", fg_color="#E67E22")
        
        os.makedirs(dest, exist_ok=True); hist = os.path.join(dest, "historico_downloads.txt")
        
        baixados = set()
        if os.path.exists(hist):
            with open(hist, "r") as f: baixados = set(f.read().splitlines())

        client = TelegramClient('sessao_trabalho', int(api_id), api_hash)
        try:
            await client.connect()
            if not await client.is_user_authorized():
                if not cod or not self.phone_code_hash: self.escrever_log("[ERRO] Peça o código na Aba 2."); return
                await client.sign_in(phone, cod, phone_code_hash=self.phone_code_hash)
            
            self.escrever_log(f"Iniciando extração do tipo: {tipo_midia.upper()}...")
            entidade = await client.get_entity(grupo_alvo)
            novos, pulados = 0, 0
            
            async for msg in client.iter_messages(entidade, limit=200):
                while self.is_paused: await asyncio.sleep(0.5)
                
                if msg.media:
                    if tipo_midia == "fotos" and not msg.photo: continue
                    elif tipo_midia == "videos" and not msg.video: continue
                    
                    if str(msg.id) in baixados: 
                        pulados += 1; continue
                        
                    novos += 1
                    self.escrever_log(f"Baixando mídia inédita (ID {msg.id})...")
                    await client.download_media(msg, file=dest)
                    with open(hist, "a") as f: f.write(f"{msg.id}\n")
                    baixados.add(str(msg.id))
                    
            self.escrever_log(f"\n[FIM DA EXTRAÇÃO ({tipo_midia.upper()})]")
            self.escrever_log(f"-> Novos arquivos baixados: {novos} | Ignorados: {pulados}")
        except Exception as e: self.escrever_log(f"[ERRO] {str(e)}")
        finally:
            await client.disconnect()
            self.btn_fotos.configure(state="normal")
            self.btn_videos.configure(state="normal")
            self.btn_ambos.configure(state="normal")
            self.btn_escolher_pasta.configure(state="normal")
            self.btn_pausar.configure(state="disabled", text="Pausar", fg_color="#7F8C8D")
            self.is_running = False

if __name__ == "__main__":
    app = AppTelegram(); app.mainloop()