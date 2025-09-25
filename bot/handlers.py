from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from memory import ShortTermMemory
from langchain_core.messages import HumanMessage, AIMessage
import os
from datetime import datetime

router = Router()
memory = ShortTermMemory()

hf_token = os.getenv("HUGGINGFACE_TOKEN")
if not hf_token:
    raise ValueError("HUGGINGFACE_TOKEN не найден в .env")
print(f"Токен загружен: {hf_token[:4]}...")

@router.message(Command("start"))
async def start(message: Message):
    await message.reply(f"Привет, {message.from_user.id}! Фитнес-бот.")

@router.message()
async def echo(message: Message):
    user_id = message.from_user.id
    mem = memory.get_memory(user_id)
    state_id = f"{str(user_id)}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    config = {"configurable": {"thread_id": str(user_id), "checkpoint_ns": "chat_history", "id": state_id}}
    state = mem.get(config)
    if state is None:
        state = {
            "id": state_id,
            "channel_values": {"messages": []},
            "channel_versions": {"messages": 0}
        }
        mem.put(config, state, metadata={}, new_versions={"messages": 0})
    else:
        state["id"] = state_id
        if "channel_values" not in state or "messages" not in state["channel_values"]:
            state["channel_values"] = {"messages": []}
        if "channel_versions" not in state:
            state["channel_versions"] = {"messages": 0}
        mem.put(config, state, metadata={}, new_versions={"messages": state["channel_versions"].get("messages", 0)})
    print(f"Состояние: {state}")
    messages = state["channel_values"]["messages"]
    messages.append(HumanMessage(content=message.text))
    messages.append(AIMessage(content=f"Эхо: {message.text}"))
    state["channel_values"]["messages"] = messages
    current_version = state["channel_versions"].get("messages", 0) + 1
    state["channel_versions"]["messages"] = current_version
    mem.put(config, state, metadata={}, new_versions={"messages": current_version})
    messages = memory.trim(user_id)
    await message.reply(f"Эхо: {message.text} (id: {user_id})\nИстория: {messages[-5:]}")