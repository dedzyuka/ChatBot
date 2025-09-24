from graph.chat_graph import graph

result = graph.invoke(
    {"messages": [{"role": "user", "content": "Привет! Меня зовут Богдан."}]},
    {"configurable": {"thread_id": "1"}}
)

print("=== Результат графа ===")
print(result)