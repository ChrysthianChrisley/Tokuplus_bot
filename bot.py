import re
import webbrowser
import logging
import os
import sys
from dotenv import load_dotenv
from telegram import Update
from telegram.error import NetworkError, TimedOut
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# --- CONFIGURAÇÃO DE AMBIENTE ---
# Carrega as variáveis do arquivo .env
load_dotenv()

# Tenta pegar o token do ambiente. Se não existir, avisa o usuário.
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    print("ERRO: A variável TELEGRAM_TOKEN não foi encontrada no arquivo .env")
    sys.exit(1)

# --- CONFIGURAÇÃO DE LOGS ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Silencia logs excessivos de bibliotecas externas
logging.getLogger("httpx").setLevel(logging.WARNING)

# --- TRATAMENTO DE ERROS ---
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ignora erros de rede comuns e loga outros erros."""
    if isinstance(context.error, (TimedOut, NetworkError)):
        return
    logger.error("Exceção não tratada:", exc_info=context.error)

# --- FUNÇÕES DE COMANDO E MENSAGEM ---

async def convidar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Detecta e-mail, abre o convite no navegador (local) e responde ao usuário.
    Nota: webbrowser.open só funciona se o bot estiver rodando na sua máquina local.
    """
    mensagem = update.message.text
    # Regex ajustado para capturar e-mails com mais precisão
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', mensagem)
    
    if email_match:
        email = email_match.group(0)
        
        # Evita loop com o próprio email do bot, se necessário
        if 'tokuplus.contact@gmail.com' not in email:
            logger.info(f"Processando convite para: {email}")

            try:
                convite_url = f"https://tokuplus.com/Robot/index.asp?email={email}"
                # Abertura do navegador no host onde o bot está rodando
                webbrowser.open(convite_url)
            except Exception as e:
                logger.error(f"Erro ao tentar abrir navegador: {e}")

            await update.message.reply_text(
                f"Convite processado para: {email}\n\n"
                "Baixe o Toku+ na Google Play e faça seu cadastro:\n"
                "https://shorturl.at/GFy1L"
            )

async def enviado(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Confirmação manual de envio."""
    await update.message.reply_text(
        "Seu convite foi enviado!\n\n"
        "Baixe o Toku+ na Google Play e faça seu cadastro:\nhttps://shorturl.at/GFy1L"
    )

async def wpp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia link do WhatsApp e deleta o comando do usuário para limpar o chat."""
    mensagem = "Acesse o grupo Toku+ pelo WhatsApp:\n\nhttps://chat.whatsapp.com/Hud6NZamWN2KSChvOHZreH"
    
    try:
        await update.message.delete()
    except Exception as e:
        logger.debug(f"Não foi possível deletar a mensagem (sem permissão?): {e}")
        
    await context.bot.send_message(chat_id=update.effective_chat.id, text=mensagem)

async def web(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Instruções para versão Web."""
    mensagem = (
        "Para acessar a versão via web:\n\n"
        "1 - Verifique se você está com doação ativa.\n"
        "    1.1 No Toku+, clique na sua imagem de perfil.\n"
        "    1.2 Vá em \"Minhas Doações\".\n\n"
        "2 - Caso esteja, acesse o site e utilize o mesmo Login do aplicativo:\n\n"
        "https://streaming.tokuplus.com/"
    )
    try:
        await update.message.delete()
    except Exception:
        pass
    await context.bot.send_message(chat_id=update.effective_chat.id, text=mensagem)

async def doacao(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Instruções para doação."""
    mensagem = (
        "Para fazer uma doação:\n\n"
        "Faça a transferência para o PIX:\n"
        "tokuplus.contact@gmail.com\n\n"
        "(Salve o comprovante)\n\n"
        "\n"
        "1. No Toku+, clique na sua imagem de perfil.\n"
        "2. Vá em \"Minhas Doações\".\n"
        "3. Escolha a opção \"Quero Ajudar\".\n"
        "4. Escolha o valor da doação realizada.\n"
        "5. Selecione o arquivo do comprovante.\n\n"
        "Será efetivado o mais rápido possível."
    )
    try:
        await update.message.delete()
    except Exception:
        pass
    await context.bot.send_message(chat_id=update.effective_chat.id, text=mensagem)

# --- FUNÇÃO PRINCIPAL ---
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    application.add_error_handler(error_handler)
    application.add_handler(CommandHandler(["navegador", "web", "computador"], web))
    application.add_handler(CommandHandler(["wpp"], wpp))
    application.add_handler(CommandHandler(["enviado"], enviado))
    application.add_handler(CommandHandler(["doacao", "ajudar", "pix"], doacao))
    
    # Handler de Texto (E-mail)
    # Regex captura texto que contenha um email
    email_filter = filters.Regex(r'[\w\.-]+@[\w\.-]+\.\w+')
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & email_filter, convidar))

    logger.info("Bot Toku+ iniciado com sucesso.")
    
    # Run polling
    application.run_polling()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Bot encerrado pelo usuário.")
    except Exception as e:
        logger.critical(f"Erro fatal na execução: {e}")