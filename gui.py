import tkinter as tk
from tkinter import simpledialog, messagebox

from Library.classes_10 import Budget
from Library import functions


class BudgetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BudgetBuddy")
        self.root.geometry("400x400")

        self.grocery = Budget("grocery")
        self.car = Budget("car")

        # Title
        tk.Label(root, text="Welcome to BudgetBuddy!", font=("Arial", 14)).pack(pady=10)

        # Name Input
        tk.Label(root, text="Enter your name:").pack()
        self.name_entry = tk.Entry(root, width=30)
        self.name_entry.pack()

        # Income Input
        tk.Label(root, text="Enter monthly income:").pack()
        self.income_entry = tk.Entry(root, width=30)
        self.income_entry.pack()

        # Buttons
        tk.Button(root, text="Add Grocery Expenses", command=self.add_grocery).pack(pady=10)
        tk.Button(root, text="Add Car Expenses", command=self.add_car).pack(pady=10)
        tk.Button(root, text="Calculate Budget", command=self.calculate).pack(pady=15)

        # Output Text Box
        self.output_box = tk.Text(root, height=8, width=45)
        self.output_box.pack(pady=10)

    def add_grocery(self):
        self.add_expenses_gui(self.grocery)

    def add_car(self):
        self.add_expenses_gui(self.car)

    def add_expenses_gui(self, budget_obj):
        try:
            num = simpledialog.askinteger("Expenses", f"How many {budget_obj.expense_type} expenses?")
            if num is None:
                return

            for i in range(num):
                entry = simpledialog.askstring(
                    "Add Expense",
                    f"Enter type and cost (Example: Milk 10):"
                )
                if entry:
                    try:
                        type_, cost = entry.split()
                        budget_obj.expenses_dict[type_] = float(cost)
                    except:
                        messagebox.showerror("Error", "Incorrect format. Use: Milk 10")
        except:
            messagebox.showerror("Error", "Input error.")

    def calculate(self):
        try:
            income = float(self.income_entry.get())
            total_expenses = sum(self.grocery.expenses_dict.values()) + sum(self.car.expenses_dict.values())

            balance = functions.calc_balance(income, total_expenses)

            # Clear output
            self.output_box.delete(1.0, tk.END)

            # Print results
            self.output_box.insert(tk.END, f"Income: ${income}\n")
            self.output_box.insert(tk.END, f"Grocery Expenses: ${sum(self.grocery.expenses_dict.values())}\n")
            self.output_box.insert(tk.END, f"Car Expenses: ${sum(self.car.expenses_dict.values())}\n")
            self.output_box.insert(tk.END, f"Total Expenses: ${total_expenses}\n")
            self.output_box.insert(tk.END, f"Balance: ${balance}\n\n")

            #Balance
            if balance > 0:
                status = "Great! You are saving money!"
            elif balance == 0:
                status = "You are breaking even."
            else:
                status = "**WARNING** You are overspending!"

            self.output_box.insert(tk.END, status)

        except:
            messagebox.showerror("Error", "Please enter a valid income number.")


# makes GUI visable 
if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetGUI(root)
    root.mainloop()
