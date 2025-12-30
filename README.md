# 🤖 TokuPlus Bot

Bot de automação e suporte desenvolvido em Python para a comunidade **Toku+**. Este projeto visa facilitar a administração de novos usuários e fornecer respostas rápidas sobre o acesso à plataforma.

## Funcionalidades

- **Automação de Convites:** O bot monitora mensagens de texto e, ao detectar um e-mail válido, executa um script local para processar o convite via navegador.
- **Comandos de Suporte:**
  - `/wpp`: Envia o link direto para o grupo do WhatsApp.
  - `/web` ou `/navegador`: Fornece instruções para acesso via streaming web.
  - `/doacao`: Informa os meios para contribuir com o projeto (PIX e app).
- **Onboarding:** Orienta novos usuários com links para download na Google Play.

## Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Biblioteca Principal:** `python-telegram-bot` (Wrapper para a API do Telegram)
- **Automação Local:** `webbrowser` (para execução de triggers via URL)
- **Gerenciamento de Ambiente:** `python-dotenv`

## Como usar

1. Clone o repositório.
2. Instale as dependências: `pip install -r requirements.txt`
3. Configure seu token no arquivo `.env`.
4. Execute o bot: `python bot.py`

---
*Nota: A funcionalidade de abrir o navegador (`webbrowser`) é executada no servidor/máquina onde o bot está hospedado, servindo como uma ferramenta de automação para o administrador.*