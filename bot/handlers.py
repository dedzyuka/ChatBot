from aiogram import Router
from aiogram.types import Message
from graph.chat_graph import graph

router = Router()

# словарь для истории сообщений по user_id
user_histories = {}

@router.message()
async def handle_message(message: Message):
    user_id = str(message.from_user.id)

    # создаем историю, если её нет
    if user_id not in user_histories:
        user_histories[user_id] = [{"role": "user", "content": message.text}]
    else:
        user_histories[user_id].append({"role": "user", "content": message.text})

    # прогоняем через граф
    result = graph.invoke(
        {"messages": user_histories[user_id]},
        {"configurable": {"thread_id": user_id}}
    )

    # сохраняем обновлённую историю
    user_histories[user_id] = result["messages"]

    # берём последний ответ модели
    ai_reply = result["messages"][-1].content
    await message.answer(ai_reply)
