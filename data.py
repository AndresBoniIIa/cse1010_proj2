import json
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random

def save_data(categories, filename="data.txt"):
    data = {}
    for cname, category in categories.items():
        data[cname] = {ename: e.cost for ename, e in category.expenses_dict.items()}
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def load_data(categories, filename="data.txt"):
    import os
    if not os.path.exists(filename):
        return
    import json
    with open(filename, "r") as f:
        data = json.load(f)
    for cname, items in data.items():
        if cname not in categories:
            from library.classes_10 import Category
            categories[cname] = Category(cname)
        for ename, cost in items.items():
            categories[cname].add_expense(ename, cost)

def create_pie_chart(categories, ax):
    ax.clear()
    if not categories:
        return
    names = list(categories.keys())
    values = [cat.total_cost() for cat in categories.values()]
    colors = [f"#{random.randint(0,0xFFFFFF):06x}" for _ in names]
    ax.pie(values, labels=names, autopct='%1.1f%%', colors=colors)
    ax.set_title("Expense Category Breakdown")
