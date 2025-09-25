from langgraph.checkpoint.memory import MemorySaver
from datetime import datetime

class ShortTermMemory:
    def __init__(self):
        self.memories = {}

    def get_memory(self, user_id):
        if user_id not in self.memories:
            self.memories[user_id] = MemorySaver()
        return self.memories[user_id]

    def trim(self, user_id, max_tokens=5000):
        memory = self.get_memory(user_id)
        state_id = f"{str(user_id)}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        config = {"configurable": {"thread_id": str(user_id), "checkpoint_ns": "chat_history", "id": state_id}}
        state = memory.get(config)
        if state is None:
            return []
        if "channel_values" not in state or "messages" not in state["channel_values"]:
            state["channel_values"] = {"messages": []}
        messages = state["channel_values"]["messages"]
        print(f"Сообщения до обрезки: {messages}")  
        state["channel_values"]["messages"] = messages 
        memory.put(config, state, metadata={}, new_versions={})
        return messages  