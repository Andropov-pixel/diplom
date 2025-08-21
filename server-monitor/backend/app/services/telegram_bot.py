from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud.user import update_user_telegram_chat_id
from app.core.config import settings
import logging
import re

logger = logging.getLogger(__name__)


class TelegramBotService:
    def __init__(self):
        self.application = None
        self.bot = None
        self.is_running = False

    async def start(self):
        """Start Telegram bot"""
        if not settings.TELEGRAM_BOT_TOKEN:
            logger.warning("Telegram bot token not configured")
            return

        try:
            self.application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
            self.bot = self.application.bot

            # Add handlers
            self.application.add_handler(CommandHandler("start", self._start_command))
            self.application.add_handler(CommandHandler("help", self._help_command))
            self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message))

            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling()

            self.is_running = True
            logger.info("Telegram bot started successfully")

        except Exception as e:
            logger.error(f"Failed to start Telegram bot: {e}")
            raise

    async def stop(self):
        """Stop Telegram bot"""
        if self.application:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
            self.is_running = False
            logger.info("Telegram bot stopped")

    async def _start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        await update.message.reply_text(
            "👋 Welcome to Server Monitor Bot!\n\n"
            "Send your verification code to connect your account."
        )

    async def _help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        await update.message.reply_text(
            "🤖 Help:\n"
            "/start - Start bot\n"
            "/help - Show help\n\n"
            "Send verification code from web platform to connect account."
        )

    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages"""
        message_text = update.message.text

        # Validate verification code format (6 digits)
        if re.match(r'^\d{6}$', message_text):
            await self._handle_verification(update, message_text)
        else:
            await update.message.reply_text("Please send a 6-digit verification code.")

    async def _handle_verification(self, update: Update, code: str):
        """Handle verification code"""
        async with get_db() as db:
            try:
                user_id = int(code)
                success = await update_user_telegram_chat_id(db, user_id, str(update.effective_chat.id))

                if success:
                    await update.message.reply_text("✅ Account connected successfully!")
                else:
                    await update.message.reply_text("❌ Invalid verification code.")

            except (ValueError, Exception) as e:
                await update.message.reply_text("❌ Error processing verification code.")
                logger.error(f"Verification error: {e}")

    async def send_notification(self, chat_id: str, message: str):
        """Send notification to user"""
        try:
            await self.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            logger.error(f"Failed to send Telegram notification: {e}")


# Global instance
telegram_bot_service = TelegramBotService()