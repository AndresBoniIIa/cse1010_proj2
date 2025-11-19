from library.classes_10 import Category
from library import functions
import data

categories = {}  # global dictionary of Category objects
last_report = ""

def add_category(name):
    if name not in categories:
        categories[name] = Category(name)

def add_expense(cat_name, expense_name, cost):
    add_category(cat_name)
    categories[cat_name].add_expense(expense_name, cost)

def delete_expense(cat_name, expense_name):
    if cat_name in categories:
        categories[cat_name].delete_expense(expense_name)

def delete_category(cat_name):
    if cat_name in categories:
        del categories[cat_name]

def calculate_budget(income_str):
    global last_report
    try:
        income = float(income_str)
    except:
        income = 0
        last_report = "Invalid income input. Defaulting to 0.\n"

    total_expenses = sum(cat.total_cost() for cat in categories.values())
    balance = functions.calc_balance(income, total_expenses)
    last_report += f"Income: ${income:.2f}\n"
    for cname, cat in categories.items():
        last_report += f"{cname} total: ${cat.total_cost():.2f}\n"
    last_report += f"Total Expenses: ${total_expenses:.2f}\n"
    last_report += f"Balance: ${balance:.2f}\n"
    last_report += functions.status(balance) + "\n"
    data.save_data(categories)

def import_export_data(root):
    from tkinter import filedialog, messagebox
    try:
        # Export
        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile="data.txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if save_path:
            data.save_data(categories, save_path)
            messagebox.showinfo("Success", "Data exported successfully!")

        # Import
        load_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if load_path:
            data.load_data(categories, load_path)
            messagebox.showinfo("Success", "Data imported successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"File operation failed:\n{e}")
