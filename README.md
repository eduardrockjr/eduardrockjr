# 📥 Automação e Extração de Mídia do Telegram (Desktop App)

Aplicação desktop desenvolvida em Python com interface gráfica moderna (CustomTkinter) e integração com a API do Telegram via **Telethon**, projetada para automatizar o rastreio e download de mídias (fotos e vídeos) de canais e grupos de forma eficiente e segura.

---

## 🚀 Funcionalidades Principais

* **Interface Gráfica Moderna (GUI):** Desenvida em `CustomTkinter` com layout em modo escuro (Dark Mode) e navegação intuitiva em abas estilo *Wizard* (Passo a Passo).
* **Processamento Assíncrono (Multithreading):** Utiliza `asyncio` e `threading` para separar as requisições de rede da interface, impedindo que a janela "congele" durante os downloads pesados.
* **Controle de Estado em Tempo Real:** Sistema interativo com botões de Pausar, Retomar e logs detalhados de progresso na própria interface.
* **Filtros Inteligentes de Mídia:** Permite selecionar o download exclusivo de fotos, vídeos ou ambos de forma simultânea.
* **Prevenção de Duplicatas:** Sistema integrado de histórico (`historico_downloads.txt`) que evita baixar o mesmo arquivo duas vezes.
* **Portabilidade:** Empacotado em um único executável (`.exe`) autossuficiente via `PyInstaller`.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.13** (Linguagem principal)
* **Telethon** (Biblioteca assíncrona para interação com a API MTProto do Telegram)
* **CustomTkinter** (Framework de UI moderno baseado no Tkinter nativo)
* **PyInstaller** (Ferramenta de empacotamento para distribuição binária)

---

## ⚙️ Como Usar (Versão Executável)

1. Faça o download da última versão disponível na aba **Releases** deste repositório.
2. Execute o arquivo `main.exe`.
3. Siga o **Passo 1** para obter gratuitamente suas credenciais (`API ID` e `API Hash`) no portal oficial do Telegram (`my.telegram.org`).
4. Preencha seus dados no **Passo 2**, solicite o código de verificação SMS e autentique-se.
5. No **Passo 3**, selecione a pasta de destino desejada e clique no tipo de mídia que deseja extrair.

---

## 👨‍💻 Desenvolvido por
**Eduardo Rocha Paukoski**  
*Profissional de Suporte de TI e Desenvolvedor em formação (Recém formado em Análise e Desenvolvimento de Sistemas)*
