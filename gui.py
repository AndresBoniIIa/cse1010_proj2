import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog

from Library.classes_10 import Budget
from Library import functions


class BudgetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BudgetBuddy")
        self.root.geometry("400x700")

        self.grocery = Budget("grocery")
        self.car = Budget("car")

        # Reset file
        with open("data.txt", "w") as file:
            file.write("BudgetBuddy Data File\n\n")

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

        # Download Button
        tk.Button(root, text="Download Data File", command=self.download_data).pack(pady=10)

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

            # Text output stored here for file writing
            text_output = (
                f"Income: ${income}\n"
                f"Grocery Expenses: ${sum(self.grocery.expenses_dict.values())}\n"
                f"Car Expenses: ${sum(self.car.expenses_dict.values())}\n"
                f"Total Expenses: ${total_expenses}\n"
                f"Balance: ${balance}\n\n"
            )

            self.output_box.insert(tk.END, text_output)

            # Status label
            if balance > 0:
                status = "Great! You are saving money!"
            elif balance == 0:
                status = "You are breaking even."
            else:
                status = "**WARNING** You are overspending!"

            self.output_box.insert(tk.END, status)

            # Write to file
            with open("data.txt", "w") as file:
                file.write("BudgetBuddy Report\n\n")
                file.write(text_output)
                file.write(status + "\n\n")
                file.write("Grocery Expense Breakdown:\n")
                for k, v in self.grocery.expenses_dict.items():
                    file.write(f" - {k}: ${v}\n")

                file.write("\nCar Expense Breakdown:\n")
                for k, v in self.car.expenses_dict.items():
                    file.write(f" - {k}: ${v}\n")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

    def download_data(self):
        try:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                initialfile="data.txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if save_path:
                with open("data.txt", "r") as src, open(save_path, "w") as dst:
                    dst.write(src.read())
                messagebox.showinfo("Success", "File downloaded successfully!")
        except:
            messagebox.showerror("Error", "Unable to save data file.")


# makes GUI visible 
if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetGUI(root)
    root.mainloop()
