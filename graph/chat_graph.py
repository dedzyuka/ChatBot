from typing import TypedDict, Annotated
from langgraph.graph import StateGraph
from bot.llm import llm
from bot.db import get_checkpointer

class State(TypedDict):
    messages: Annotated[list[dict], "Chat messages"]

def chat_node(state: State) -> State:
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}

# Подключаем чекпоинтер
checkpointer = get_checkpointer()

# Строим граф
builder = StateGraph(State)
builder.add_node("chat", chat_node)
builder.set_entry_point("chat")
builder.set_finish_point("chat")

graph = builder.compile(checkpointer=checkpointer)
