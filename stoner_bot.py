import os
from dotenv import load_dotenv
import logging
import random
import json
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
)
load_dotenv()
api_key = os.getenv("API_KEY")
# Logging Setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot States
ASKING, FINISHED = range(2)

# Load Questions
QUESTIONS_FILE = "questions.json"
with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
    QUESTION_POOL = json.load(file)

# Images Folder
IMAGES_FOLDER = "images"

# Start Command
async def start(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    user_name = update.effective_user.full_name
    logger.info(f"User {user_name} (ID: {user_id}) started the bot.")

    context.user_data[user_id] = {
        "questions": random.sample(QUESTION_POOL, 10),
        "answers": [],
        "yes_count": 0,
        "current_question": 0,
    }

    keyboard = [[InlineKeyboardButton("Почати тест", callback_data="start_quiz")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "<b>Привіт! Це бот для визначення наскільки ти упоровся 🌿😵‍💫.\nНатисніть 'Почати тест'</b>!",
        reply_markup=reply_markup,
        parse_mode="HTML",
    )
    logger.info("Sent 'Почати тест' button.")
    return ASKING

# Handle Start Quiz Button
async def handle_start_quiz(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user_id = query.from_user.id
    user_name = query.from_user.full_name
    await query.answer()
    logger.info(f"User {user_name} (ID: {user_id}) clicked 'Почати'. Starting quiz.")
    await ask_question(update, context)
    return ASKING

# Ask Question
async def ask_question(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    user_name = query.from_user.full_name
    user_data = context.user_data.get(user_id)

    if not user_data:
        logger.warning(f"User {user_name} (ID: {user_id}) has no active session.")
        await query.message.reply_text("Щось пішло не так. Спробуйте почати знову /start.")
        return ConversationHandler.END

    current_question_index = user_data["current_question"]
    if current_question_index < len(user_data["questions"]):
        question = user_data["questions"][current_question_index]
        logger.info(f"User {user_name} (ID: {user_id}) is being asked: {question}")
        keyboard = [
            [InlineKeyboardButton("Так", callback_data="yes"), InlineKeyboardButton("Ні", callback_data="no")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            f"<b>{question}</b>",
            reply_markup=reply_markup,
            parse_mode="HTML",
        )
    else:
        logger.info(f"User {user_name} (ID: {user_id}) has answered all questions.")
        await finish_quiz(update, context)

# Handle Answer
async def handle_answer(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    user_name = query.from_user.full_name
    user_data = context.user_data.get(user_id)

    if not user_data or "current_question" not in user_data:
        logger.warning(f"User {user_name} (ID: {user_id}) has no active session.")
        await query.message.reply_text("Щось пішло не так. Спробуйте почати знову /start.")
        return ConversationHandler.END

    if user_data["current_question"] >= len(user_data["questions"]):
        logger.error(
            f"User {user_name} (ID: {user_id}) encountered an out-of-bounds question index. "
            f"Index: {user_data['current_question']}, Questions Length: {len(user_data['questions'])}"
        )
        return await restart(update, context)

    answer = "Так" if query.data == "yes" else "Ні"
    user_data["answers"].append(
        {"question": user_data["questions"][user_data["current_question"]], "answer": answer}
    )
    if query.data == "yes":
        user_data["yes_count"] += 1

    logger.info(f"User {user_name} (ID: {user_id}) answered: {answer}")
    user_data["current_question"] += 1

    if user_data["current_question"] < len(user_data["questions"]):
        await ask_question(update, context)
    else:
        logger.info(f"User {user_name} (ID: {user_id}) finished answering questions.")
        await finish_quiz(update, context)
    return ASKING

# Finish Quiz
async def finish_quiz(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user_id = query.from_user.id
    user_name = query.from_user.full_name
    user_data = context.user_data.get(user_id)

    if not user_data:
        logger.warning(f"User {user_name} (ID: {user_id}) has no active session.")
        await query.message.reply_text("Щось пішло не так. Спробуйте почати знову /start.")
        return ConversationHandler.END

    yes_count = user_data["yes_count"]

    if yes_count <= 3:
        summary = random.choice([
        "🟢 <b>Лайт-наркоша</b>: Ти ще не сильно упоровся, але твої очі вже трохи червоні!",
        "🟢 <b>Майже норм</b>: Ти точно знаєш межу, але краще не ризикуй!",
        "🟢 <b>Кежуал</b>: Дим навколо тебе лише зрідка, не час переходити на новий рівень!",
        "🟢 <b>На межі</b>: Ти ще не торч, але точно знаєш, як це виглядає.",
        "🟢 <b>Контрольований</b>: Ти більше схожий на спостерігача, ніж на справжнього упоротого."
    ])
    elif 4 <= yes_count <= 6:
        summary = random.choice([
        "🟡 <b>Середній фіт</b>: У твоїй компанії тебе вже називають «димовий генератор»!",
        "🟡 <b>Досвідчений</b>: У тебе є стиль, і це знають усі, хто поруч.",
        "🟡 <b>Вже наркєт</b>: Твої друзі скидаються тобі на нову пачку, бо ти не зупиняєшся.",
        "🟡 <b>Бувалий</b>: Дим і фани завжди поруч, навіть якщо ти цього не помічаєш.",
        "🟡 <b>Починається</b>: Всі знають, що ти любиш тему, і це вже серйозно."
    ])
    else:
        summary = random.choice([
        "🔴 <b>ТОП ТОРЧ!</b>: Ти — легенда, димовий бог, такий, як ти, запалює всіх навколо!",
        "🔴 <b>Майстер упоротих</b>: Усі чекають на твої нові рекорди.",
        "🔴 <b>Божевільний</b>: У твоєму оточенні немає тих, хто б міг переплюнути тебе.",
        "🔴 <b>НаркоЛорд</b>: Ти став іконою всіх торчків! Всі знають, хто тут головний.",
        "🔴 <b>Димовий король</b>: Коли ти поруч, повітря стає важчим, а атмосфера густішою."
    ])


    image_path = f"{IMAGES_FOLDER}/420_{random.randint(1, 20)}.jpg"
    logger.info(f"User {user_name} (ID: {user_id}) will receive image: {image_path}")
    try:
        with open(image_path, "rb") as img:
            await query.message.reply_photo(photo=img, caption=summary, parse_mode="HTML")
    except FileNotFoundError:
        logger.error(f"Image not found: {image_path}")
        await query.message.reply_text(summary + "\n\nНе вдалося знайти зображення 😢", parse_mode="HTML")

    keyboard = [[InlineKeyboardButton("Почати заново", callback_data="restart")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("<b>Хочете спробувати ще раз?</b>", reply_markup=reply_markup, parse_mode="HTML")
    return FINISHED

# Restart Quiz with Full Reset
async def restart(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    user_id = query.from_user.id
    user_name = query.from_user.full_name
    await query.answer()

    logger.info(f"User {user_name} (ID: {user_id}) clicked 'Почати заново'. Restarting the quiz.")

    context.user_data[user_id] = {
        "questions": random.sample(QUESTION_POOL, 10),
        "answers": [],
        "yes_count": 0,
        "current_question": 0,
    }

    keyboard = [[InlineKeyboardButton("Почати тест", callback_data="start_quiz")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "<b>Привіт! Це бот для визначення наскільки ти упоровся</b> 🌿😵‍💫.\n <b>Натисніть 'Почати тест'</b>!",
        reply_markup=reply_markup,
        parse_mode="HTML",
    )
    logger.info("Sent 'Почати тест' button for restart.")
    return ASKING

# Global error handler
async def error_handler(update: object, context: CallbackContext):
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

# Main Code
if __name__ == "__main__":
    TOKEN = api_key
    application = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASKING: [CallbackQueryHandler(handle_answer)],
            FINISHED: [CallbackQueryHandler(restart, pattern="^restart$")],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(CallbackQueryHandler(handle_start_quiz, pattern="^start_quiz$"))
    application.add_handler(conv_handler)

    logger.info("Bot is running...")
    application.run_polling()
