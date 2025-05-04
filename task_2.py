import os
import pandas as pd
from BTrees.OOBTree import OOBTree
import timeit

df = pd.read_csv("/Users/anndunska/Downloads/generated_items_data.csv")
print(df.head())

# Ініціалізація структур
tree = OOBTree()
dictionary  = {}

# Функція для додавання товару
def add_item_to_tree(tree, price, item):
    if price in tree:
        tree[price].append(item)
    else:
        tree[price] = [item]

# Функція для додавання товару до dict
def add_item_to_dict(dictionary, key, name, category, price):
    item = {
        'Name': name,
        'Category': category,
        'Price': price
    }
    dictionary[key] = item
    
# Додавання датафрейму до обох структур
for _, row in df.iterrows():
    item = {
        'ID': row.ID,
        'Name': row.Name,
        'Category': row.Category,
        'Price': row.Price
    }
    add_item_to_tree(tree, row.Price, item)
    add_item_to_dict(dictionary, row.ID, row.Name, row.Category, row.Price)

print(tree[320.07])   
print(dictionary[1]) 

# Функція пошуку товарів у визначеному діапазоні цін для BTrees
def range_query_tree(tree, lower_border, upper_border):
    results = {}

    for price, items in tree.items(lower_border, upper_border):
        for item in items:
            results[item["ID"]] = item
    return results

# Функція пошуку товарів у визначеному діапазоні цін для dict
def range_query_dict(dictionary, lower_border, upper_border):
    results  = {}

    for key, item in dictionary.items():
        if lower_border <= item["Price"] <= upper_border:
            results[key] = item
    return results

# Тестування пошуку для обох структур
tree_results = range_query_tree(tree, 2.4, 2.41)
dict_results = range_query_dict(dictionary, 2.4, 2.41)

print("Tree results:", tree_results)
print("Dict results:", dict_results)

# Замір часу
tree_time = timeit.timeit(lambda: range_query_tree(tree, 2.4, 2.41), number=100)
dict_time = timeit.timeit(lambda: range_query_dict(dictionary, 2.4, 2.41), number=100)

print(f"Average time per request for OOBTree: {tree_time / 100:.8f} seconds")
print(f"Average time per request for Dict: {dict_time / 100:.8f} seconds")

print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
print(f"Total range_query time for Dict: {dict_time:.6f} seconds")
