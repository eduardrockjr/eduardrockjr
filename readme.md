# Canivete Suíço de Reconhecimento (Telegram Edition)

Ferramenta em Python com interface gráfica desenvolvida para testes de reconhecimento (Recon/OSINT) e análise de segurança de aplicações web.

## 🚀 Funcionalidades
- **Clickjacking Check**: Verifica a presença dos cabeçalhos `X-Frame-Options` e `Content-Security-Policy`.
- **Cookies Check**: Analisa se os cookies utilizam as flags de segurança `Secure` e `HttpOnly`.
- **HSTS & Security Headers**: Checa cabeçalhos `Strict-Transport-Security` e `X-Content-Type-Options`.
- **Servidor & IP**: Identifica o IP do host, software do servidor e tecnologias do backend.
- **Análise do robots.txt**: Leitura e exploração automatizada de rotas e caminhos restritos.
- **Mapeamento de Subdomínios (OSINT)**: Consulta passiva de certificados SSL/TLS no `crt.sh`.

## 🛠️ Como Executar

### Pré-requisitos
- Python 3.x instalado

### Passo a Passo
1. Clone o repositório:
   ```bash
   git clone [https://github.com/SEU_USUARIO/canivetepentest.git](https://github.com/SEU_USUARIO/canivetepentest.git)
   cd canivetepentest

   ⚠️ Isenção de Responsabilidade
Esta ferramenta foi criada exclusivamente para fins educacionais e testes de segurança autorizados. O uso indevido em sistemas sem prévia autorização é de inteira responsabilidade do usuário.