from library.classes_10 import Category
from library import functions
import data

categories = {}  # global dictionary of Category objects
last_report = ""

def add_category(name):
    if not name:
        return

    raw = name.strip()

    # Find if a case-insensitive match already exists
    for existing in categories:
        if existing.lower() == raw.lower():
            return  # category already exists, do nothing

    # Otherwise create a NEW category using the original casing the user typed
    categories[raw] = Category(raw)

def add_expense(cat_name, exp_name, cost):
    if not cat_name:
        return

    raw = cat_name.strip()

    # Find matching category (case-insensitive)
    for existing in categories:
        if existing.lower() == raw.lower():
            categories[existing].add_expense(exp_name, cost)
            return

    # If no existing category matched, create a new one
    categories[raw] = Category(raw)
    categories[raw].add_expense(exp_name, cost)

def delete_category(cat_name):
    if cat_name in categories:
        del categories[cat_name]

def calculate_budget(income_str):
    global last_report
    last_report = ""   # <-- RESET THE REPORT EACH TIME

    try:
        income = float(income_str)
    except:
        last_report = "**ERROR** Invalid Income Input **ERROR**\n"   # Only error message
        return  # <-- Stop here so no other output is added

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
