import tkinter as tk
from tkinter import ttk 
from tkinter import simpledialog, messagebox, filedialog

from library.classes_10 import Budget 
from library import functions


class BudgetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BudgetBuddy")
        self.root.geometry("400x700")

        UCONN_NAVY = "#000E2F"
        UCONN_WHITE = "#FFFFFF"
        UCONN_RED = "#EF3E42"
        
        self.root.configure(bg=UCONN_NAVY)

        style = ttk.Style()
        
        style.theme_use('clam') 

        style.configure("Main.TFrame", background=UCONN_NAVY)
        
        style.configure("TLabel", 
                        background=UCONN_NAVY, 
                        foreground=UCONN_WHITE, 
                        font=('Helvetica', 12))
        
        style.configure("Title.TLabel",
                        background=UCONN_NAVY,
                        foreground=UCONN_WHITE,
                        font=('Helvetica', 18, "bold"))
        
        style.configure("TButton", 
                        font=('Helvetica', 12, 'bold'),
                        padding=10,
                        background="#f0f0f0",
                        foreground="#333")
        style.map("TButton",
                  background=[('active', '#ddd'), ('!disabled', '#f0f0f0')])

        style.configure("Accent.TButton", 
                        background=UCONN_RED,
                        foreground=UCONN_WHITE,
                        font=('Helvetica', 12, 'bold'),
                        padding=10,
                        borderwidth=0)
        style.map("Accent.TButton",
                  background=[('active', '#D03030'), ('!disabled', UCONN_RED)])
        
        style.configure("TEntry",
                        fieldbackground="white",
                        foreground="black",
                        borderwidth=1,
                        padding=5)

        content_frame = ttk.Frame(root, padding="20 20 20 20", style="Main.TFrame")
        content_frame.pack(fill="both", expand=True)

        self.grocery = Budget("grocery")
        self.car = Budget("car")
        self.load_data_from_file() 

        ttk.Label(content_frame, text="Welcome to BudgetBuddy!", style="Title.TLabel").pack(pady=10)

        ttk.Label(content_frame, text="Enter your name:", style="TLabel").pack(pady=(10, 2), anchor='w')
        self.name_entry = ttk.Entry(content_frame, width=30)
        self.name_entry.pack(pady=(0, 10), fill='x')

        ttk.Label(content_frame, text="Enter monthly income:", style="TLabel").pack(pady=(10, 2), anchor='w')
        self.income_entry = ttk.Entry(content_frame, width=30)
        self.income_entry.pack(pady=(0, 10), fill='x')

        ttk.Button(content_frame, text="Add Grocery Expenses", command=self.add_grocery, style="TButton").pack(pady=10, fill='x')
        ttk.Button(content_frame, text="Add Car Expenses", command=self.add_car, style="TButton").pack(pady=10, fill='x')
        ttk.Button(content_frame, text="Calculate Budget", command=self.calculate, style="Accent.TButton").pack(pady=15, fill='x')
        ttk.Button(content_frame, text="Download Data File", command=self.download_data, style="TButton").pack(pady=10, fill='x')

        self.output_box = tk.Text(
            content_frame, 
            height=8, 
            width=45,
            background="#001a4d",
            foreground=UCONN_WHITE,
            borderwidth=0,
            relief="flat",
            font=('Helvetica', 11),
            padx=10,
            pady=10,
            insertbackground=UCONN_WHITE
        )
        self.output_box.pack(pady=10, fill='both', expand=True)

    def load_data_from_file(self):
        try:
            with open("expenses.csv", "r") as data_file:
                for line in data_file:
                    parts = line.strip().split(',')
                    
                    if len(parts) == 3:
                        category = parts[0]
                        item = parts[1]
                        cost = float(parts[2])
                        
                        if category == "grocery":
                            self.grocery.expenses_dict[item] = cost
                        elif category == "car":
                            self.car.expenses_dict[item] = cost
        
        except FileNotFoundError:
            pass 
        except Exception as e:
            messagebox.showerror("Load Error", f"Could not load saved data: {e}")

    def add_grocery(self):
        self.add_expenses_gui(self.grocery)

    def add_car(self):
        self.add_expenses_gui(self.car)

    def add_expenses_gui(self, budget_obj):
        try:
            num = simpledialog.askinteger("Expenses", f"How many {budget_obj.expense_type} expenses?")
            if num is None:
                return

            if budget_obj.expense_type == "car":
                example_text = "Example: repair 200"
            elif budget_obj.expense_type == "grocery":
                example_text = "Example: Milk 10"
            else:
                example_text = "Example: Item 10"

            for i in range(num):
                entry = simpledialog.askstring(
                    "Add Expense",
                    f"Enter type and cost ({example_text}):"
                )
                if entry:
                    try:
                        parts = entry.split()
                        cost = float(parts[-1]) 
                        type_ = " ".join(parts[:-1]) 
                        
                        if not type_:
                            messagebox.showerror("Error", f"Incorrect format. Use: {example_text}")
                            continue

                        budget_obj.expenses_dict[type_] = float(cost)
                    except:
                        messagebox.showerror("Error", f"Incorrect format. Use: {example_text}")
        except:
            messagebox.showerror("Error", "Input error.")

    def calculate(self):
        try:
            income_str = self.income_entry.get()
            income = float(income_str) if income_str else 0.0
            
            total_expenses = sum(self.grocery.expenses_dict.values()) + sum(self.car.expenses_dict.values())
            balance = functions.calc_balance(income, total_expenses)

            self.output_box.delete(1.0, tk.END)

            text_output = (
                f"Income: ${income:.2f}\n"
                f"Grocery Expenses: ${sum(self.grocery.expenses_dict.values()):.2f}\n"
                f"Car Expenses: ${sum(self.car.expenses_dict.values()):.2f}\n"
                f"Total Expenses: ${total_expenses:.2f}\n"
                f"Balance: ${balance:.2f}\n\n"
            )

            self.output_box.insert(tk.END, text_output)

            if balance > 0:
                status = "Great! You are saving money!"
            elif balance == 0:
                status = "You are breaking even."
            else:
                status = "**WARNING** You are overspending!"

            self.output_box.insert(tk.END, status)

            with open("data.txt", "w") as file:
                file.write("BudgetBuddy Report\n\n")
                file.write(text_output)
                file.write(status + "\n\n")
                file.write("Grocery Expense Breakdown:\n")
                for k, v in self.grocery.expenses_dict.items():
                    file.write(f" - {k}: ${v:.2f}\n")

                file.write("\nCar Expense Breakdown:\n")
                for k, v in self.car.expenses_dict.items():
                    file.write(f" - {k}: ${v:.2f}\n")

            with open("expenses.csv", "w") as data_file:
                for item, cost in self.grocery.expenses_dict.items():
                    data_file.write(f"grocery,{item},{cost}\n")
                
                for item, cost in self.car.expenses_dict.items():
                    data_file.write(f"car,{item},{cost}\n")

        except ValueError:
             messagebox.showerror("Error", "Income must be a valid number.")
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


if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetGUI(root)
    root.mainloop()
