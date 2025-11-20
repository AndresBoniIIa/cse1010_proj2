import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import data
import library.functions
import library.project_10 as logic
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random

class BudgetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BudgetBuddy")
        self.root.geometry("500x700")  # larger to fit chart

        # Colors
        UCONN_NAVY = "#000E2F"
        UCONN_WHITE = "#FFFFFF"
        UCONN_RED = "#EF3E42"
        self.root.configure(bg=UCONN_NAVY)

        # Styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Main.TFrame", background=UCONN_NAVY)
        style.configure("TLabel", background=UCONN_NAVY, foreground=UCONN_WHITE, font=('Helvetica', 12))
        style.configure("Title.TLabel", background=UCONN_NAVY, foreground=UCONN_WHITE, font=('Helvetica', 18, "bold"))
        style.configure("TButton", font=('Helvetica', 12, 'bold'), padding=10, background="#f0f0f0", foreground="#333")
        style.map("TButton", background=[('active', '#ddd'), ('!disabled', '#f0f0f0')])
        style.configure("Accent.TButton", background=UCONN_RED, foreground=UCONN_WHITE, font=('Helvetica', 12, 'bold'), padding=10, borderwidth=0)
        style.map("Accent.TButton", background=[('active', '#D03030'), ('!disabled', UCONN_RED)])
        style.configure("TEntry", fieldbackground="white", foreground="black", borderwidth=1, padding=5)

        # Tabs
        self.tab_control = ttk.Notebook(root)
        self.main_tab = ttk.Frame(self.tab_control, style="Main.TFrame")
        self.chart_tab = ttk.Frame(self.tab_control, style="Main.TFrame")
        self.tab_control.add(self.main_tab, text="Main")
        self.tab_control.add(self.chart_tab, text="Category Chart")
        self.tab_control.pack(expand=1, fill="both")

        # Build tabs
        self.build_main_tab()
        self.build_chart_tab()

    
    def build_main_tab(self):
        ttk.Label(self.main_tab, text="Welcome to BudgetBuddy!", style="Title.TLabel").pack(pady=10)
        ttk.Label(self.main_tab, text="Enter your name:", style="TLabel").pack(pady=(10,2), anchor='w')
        self.name_entry = ttk.Entry(self.main_tab, width=30)
        self.name_entry.pack(pady=(0,10), fill='x')

        ttk.Label(self.main_tab, text="Enter monthly income:", style="TLabel").pack(pady=(10,2), anchor='w')
        self.income_entry = ttk.Entry(self.main_tab, width=30)
        self.income_entry.pack(pady=(0,10), fill='x')

        ttk.Button(self.main_tab, text="Add Category / Expense", command=self.add_expense_dialog, style="TButton").pack(pady=10, fill='x')
        ttk.Button(self.main_tab, text="Manage Expenses", command=self.manage_expenses_dialog, style="TButton").pack(pady=10, fill='x')
        ttk.Button(self.main_tab, text="Calculate Budget", command=self.calculate, style="Accent.TButton").pack(pady=15, fill='x')
        ttk.Button(self.main_tab, text="Import / Export Data", command=self.import_export_dialog, style="TButton").pack(pady=10, fill='x')

        self.output_box = tk.Text(
            self.main_tab,
            height=8,
            width=45,
            background="#001a4d",
            foreground="#FFFFFF",
            borderwidth=0,
            relief="flat",
            font=('Helvetica', 11),
            padx=10,
            pady=10,
            insertbackground="#FFFFFF"
        )
        self.output_box.pack(pady=10, fill='both', expand=True)

    
    def build_chart_tab(self):
        self.fig, self.ax = plt.subplots(figsize=(5,4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_tab)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        self.update_chart()

    
    def add_expense_dialog(self):
        # Ask for category 
        while True:
            category = simpledialog.askstring("Category", "Enter new or existing category name:")
            if category is None:
                return
            category = category.strip()
            if category:
                break
            messagebox.showerror("Error", "Category name cannot be empty.")

        # Ask how many expenses to add to this category
        count = simpledialog.askinteger(
            "How many?",
            f"How many expenses do you want to add to '{category}'?",
            minvalue=1
        )
        if count is None:
            return

        # Loop to collect each expense's name and cost
        for i in range(count):
            # Get expense name
            while True:
                exp_name = simpledialog.askstring("Expense Name", f"Enter name for expense #{i+1}: (e.g., oil):")
                if exp_name is None:
                    # user cancelled -> stop the whole add process
                    return
                exp_name = exp_name.strip()
                if exp_name:
                    break
                messagebox.showerror("Error", "Expense name cannot be empty.")

            # Get expense cost
            while True:
                try:
                    cost = simpledialog.askfloat("Expense Cost", f"Enter cost for '{exp_name}': (No $ sign)")
                    if cost is None:
                        # user cancelled -> stop the whole add process
                        return
                    # success: add expense
                    logic.add_expense(category, exp_name, cost)
                    messagebox.showinfo("Success", f"Added expense '{exp_name}' (${cost:.2f}) to category '{category}'")
                    break
                except:
                    messagebox.showerror("Error", "Invalid number. Enter a valid cost for the expense.")

    # Refresh chart after adding all requested expenses
        self.update_chart()

    
    def manage_expenses_dialog(self):
        categories = list(logic.categories.keys())
        if not categories:
            messagebox.showinfo("Info", "No categories available")
            return

        while True:
            category = simpledialog.askstring("Category", f"Available categories:\n{', '.join(categories)}\nSelect category:")
            if category is None:
                return
            category = category.strip()
            if category in logic.categories:
                budget = logic.categories[category]
                break
            messagebox.showerror("Error", "Category does not exist. Please try again.")

        while True:
            action = simpledialog.askstring("Action", "Type 'edit', 'delete', or 'deletecat':")
            if action is None:
                return
            action = action.lower().strip()
            if action in ["edit", "delete", "deletecat"]:
                break
            messagebox.showerror("Error", "Invalid action. Enter edit, delete, or deletecat.")

        if action == "edit":
            expenses = list(budget.expenses_dict.keys())
            if not expenses:
                messagebox.showinfo("Info", "No expenses to edit in this category")
                return
            while True:
                item = simpledialog.askstring("Edit Expense", f"Select expense to edit:\n{', '.join(expenses)}")
                if item is None:
                    return
                if item in budget.expenses_dict:
                    break
                messagebox.showerror("Error", "Expense not found. Try again.")

            while True:
                try:
                    cost = simpledialog.askfloat("Edit Expense", f"Enter new cost for '{item}':")
                    if cost is None:
                        return
                    budget.edit_expense(item, cost)
                    break
                except:
                    messagebox.showerror("Error", "Invalid number. Enter a valid cost.")

        elif action == "delete":
            expenses = list(budget.expenses_dict.keys())
            if not expenses:
                messagebox.showinfo("Info", "No expenses to delete in this category")
                return
            while True:
                item = simpledialog.askstring("Delete Expense", f"Select expense to delete:\n{', '.join(expenses)}")
                if item is None:
                    return
                if item in budget.expenses_dict:
                    logic.delete_expense(category, item)
                    break
                messagebox.showerror("Error", "Expense not found. Try again.")

        elif action == "deletecat":
            confirm = messagebox.askyesno("Confirm Delete", f"Delete entire '{category}' category?")
            if confirm:
                logic.delete_category(category)

        self.update_chart()

    
    def calculate(self):
        logic.calculate_budget(self.income_entry.get())
        self.update_output()
        self.update_chart()

    def update_output(self):
        self.output_box.delete(1.0, tk.END)
        self.output_box.insert(tk.END, logic.last_report)

    #Import / Export
    def import_export_dialog(self):
        logic.import_export_data(self.root)
        self.update_output()
        self.update_chart()

    # Pie Chart 
    def update_chart(self):
        data.create_pie_chart(logic.categories, self.ax)
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetGUI(root)
    root.mainloop()
