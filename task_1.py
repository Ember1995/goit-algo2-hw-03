from collections import deque
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

# Вершини для зручності:
# 0 – Термінал 1, 1 – Термінал 2
# 2–5 – Склади 1–4
# 6–19 – Магазини 1–14

edges = [
    # Термінали → Склади
    (0, 2, 25), (0, 3, 20), (0, 4, 15),
    (1, 4, 15), (1, 5, 30), (1, 3, 10),

    # Склади → Магазини
    (2, 6, 15), (2, 7, 10), (2, 8, 20),
    (3, 9, 15), (3, 10, 10), (3, 11, 25),
    (4, 12, 20), (4, 13, 15), (4, 14, 10),
    (5, 15, 20), (5, 16, 10), (5, 17, 15),
    (5, 18, 5), (5, 19, 10),
]

G.add_weighted_edges_from(edges)

# Позиції на основі картинки
pos = {
    0: (0, 2),  # Термінал 1
    1: (0, 1),  # Термінал 2
    2: (2, 2.5), 3: (2, 2), 4: (2, 1.5), 5: (2, 1),  # Склади
    6: (4, 3), 7: (4, 2.8), 8: (4, 2.6),  # Магазини 1–3
    9: (4, 2.4), 10: (4, 2.2), 11: (4, 2),  # Магазини 4–6
    12: (4, 1.8), 13: (4, 1.6), 14: (4, 1.4),  # Магазини 7–9
    15: (4, 1.2), 16: (4, 1), 17: (4, 0.8), 18: (4, 0.6), 19: (4, 0.4),  # Магазини 10–14
}

labels = {i: f"Термінал {i+1}" if i < 2 else f"Склад {i-1}" if i < 6 else f"Магазин {i-5}" for i in G.nodes}

plt.figure(figsize=(14, 6))
nx.draw(G, pos, with_labels=True, labels=labels, node_size=1600, node_color="skyblue", font_size=10, font_weight="bold", arrows=True)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.title("Логістична мережа")
plt.axis("off")

# Зберігаємо зображення
plt.savefig("logistics_network.png", format="png")
plt.show()

# Записуємо в readme
readme_text = ""
readme_text += "\n## Візуалізація логістичної мережі\n\n"
readme_text += "![Логістична мережа](logistics_network.png)\n"

with open("README_task1.md", "w", encoding="utf-8") as f:
    f.write(readme_text)

# Функція для пошуку збільшуючого шляху (BFS)
def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True

    while queue:
        current_node = queue.popleft()
        
        for neighbor in range(len(capacity_matrix)):
            # Перевірка, чи є залишкова пропускна здатність у каналі
            if not visited[neighbor] and capacity_matrix[current_node][neighbor] - flow_matrix[current_node][neighbor] > 0:
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)
    
    return False

# Основна функція для обчислення максимального потоку
def edmonds_karp(capacity_matrix, source, sink):
    num_nodes = len(capacity_matrix)
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]  # Ініціалізуємо матрицю потоку нулем
    parent = [-1] * num_nodes
    max_flow = 0

    # Поки є збільшуючий шлях, додаємо потік
    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        # Знаходимо мінімальну пропускну здатність уздовж знайденого шляху (вузьке місце)
        path_flow = float('Inf')
        current_node = sink

        while current_node != source:
            previous_node = parent[current_node]
            path_flow = min(path_flow, capacity_matrix[previous_node][current_node] - flow_matrix[previous_node][current_node])
            current_node = previous_node
        
        # Оновлюємо потік уздовж шляху, враховуючи зворотний потік
        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow
            current_node = previous_node
        
        # Збільшуємо максимальний потік
        max_flow += path_flow

    return max_flow

# Матриця пропускної здатності для каналів у мережі (capacity_matrix)
capacity_matrix = [
    #  T1  T2  S1  S2  S3  S4  M1  M2  M3  M4  M5  M6  M7  M8  M9  M10 M11 M12 M13 M14
    [  0,  0, 25, 20, 15,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,   0,  0,  0,  0,  0],  # Термінал 1
    [  0,  0,  0, 10, 15, 30,  0,  0,  0,  0,  0,  0,  0,  0,  0,   0,  0,  0,  0,  0],  # Термінал 2
    [  0,  0,  0,  0,  0,  0, 15, 10, 20,  0,  0,  0,  0,  0,  0,   0,  0,  0,  0,  0],  # Склад 1
    [  0,  0,  0,  0,  0,  0,  0,  0,  0, 15, 10, 25,  0,  0,  0,   0,  0,  0,  0,  0],  # Склад 2
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 20, 15, 10,   0,  0,  0,  0,  0],  # Склад 3
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  20, 10, 15,  5, 10],  # Склад 4
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,   0,  0,  0,  0,  0],  # Магазин 1
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,   0,  0,  0,  0,  0],  # Магазин 2
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,   0,  0,  0,  0,  0],  # Магазин 3
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,   0,  0,  0,  0,  0],  # Магазин 4
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,   0,  0,  0,  0,  0],  # Магазин 5
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,   0,  0,  0,  0,  0],  # Магазин 6
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,   0,  0,  0,  0,  0],  # Магазин 7
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,   0,  0,  0,  0,  0],  # Магазин 8
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,   0,  0,  0,  0,  0],  # Магазин 9
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,   0,  0,  0,  0,  0],  # Магазин 10
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,   0,  0,  0,  0,  0],  # Магазин 11
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,   0,  0,  0,  0,  0],  # Магазин 12
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,   0,  0,  0,  0,  0],  # Магазин 13
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,   0,  0,  0,  0,  0]   # Магазин 14
]

flow_data = []  # для DataFrame
readme_text += "## Потоки між терміналами і магазинами:\n\n| Термінал | Магазин | Потік (одиниць) |\n|----------|---------|------------------|\n"

for terminal in [0, 1]:
    for store in range(6, 20):
        max_flow = edmonds_karp(capacity_matrix, terminal, store)
        readme_text += f"| Термінал {terminal+1} | Магазин {store-5} | {max_flow} |\n"
        flow_data.append({
            "Термінал": f"Термінал {terminal+1}",
            "Магазин": f"Магазин {store-5}",
            "Потік": max_flow
        })

# Зберігаємо таблицю в readme
with open("README_task1.md", "w", encoding="utf-8") as f:
    f.write(readme_text)

# Створюємо DataFrame для подальшого аналізу
df = pd.DataFrame(flow_data)

# Створюємо зведену таблицю та сортуємо
pivot = df.groupby("Магазин")["Потік"].max().reset_index()
pivot = pivot.rename(columns={"Потік": "MAX of Потік"})
pivot = pivot.sort_values(by="MAX of Потік", ascending=False)

# Додаємо заголовок для зведеної таблиці
readme_text += "\n## Зведена таблиця: Максимальний потік до кожного магазину\n\n"
readme_text += "| Магазин | MAX of Потік |\n"
readme_text += "|---------|---------------|\n"

# Додаємо до readme
for _, row in pivot.iterrows():
    readme_text += f"| {row['Магазин']} | {row['MAX of Потік']} |\n"

with open("README_task1.md", "w", encoding="utf-8") as f:
    f.write(readme_text)
