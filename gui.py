import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog

# Make sure your 'classes_10.py' file is in the 'library' folder
from library.classes_10 import Budget 
from library import functions


class BudgetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BudgetBuddy")
        self.root.geometry("400x700")

        self.grocery = Budget("grocery")
        self.car = Budget("car")

        # Load any previously saved data on startup
        self.load_data_from_file() 

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

    def load_data_from_file(self):
        try:
            # We load from "expenses.csv", a file just for data
            with open("expenses.csv", "r") as data_file:
                for line in data_file:
                    # 'grocery,Milk,10.0\n' -> ['grocery', 'Milk', '10.0']
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
            # This is not an error. It just means it's the first time
            # you are running the program, so no file exists yet.
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

            # --- THIS IS THE UPDATED PART ---
            # Set the example text based on the category
            if budget_obj.expense_type == "car":
                example_text = "Example: repair 200"
            elif budget_obj.expense_type == "grocery":
                example_text = "Example: Milk 10"
            else:
                example_text = "Example: Item 10" # A good default
            # --- END OF UPDATE ---

            for i in range(num):
                entry = simpledialog.askstring(
                    "Add Expense",
                    # Use the new example_text variable
                    f"Enter type and cost ({example_text}):"
                )
                if entry:
                    try:
                        # This logic allows for multi-word types like "car repair"
                        parts = entry.split()
                        cost = float(parts[-1]) # The cost is the last part
                        type_ = " ".join(parts[:-1]) # The type is everything else
                        
                        budget_obj.expenses_dict[type_] = float(cost)
                    except:
                        messagebox.showerror("Error", f"Incorrect format. Use: {example_text}")
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

            # --- WRITE REPORT TO data.txt ---
            # This file is the "pretty" report for the user
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

            # --- SAVE RAW DATA TO expenses.csv ---
            # This file is for the program to read next time
            with open("expenses.csv", "w") as data_file:
                for item, cost in self.grocery.expenses_dict.items():
                    data_file.write(f"grocery,{item},{cost}\n")
                
                for item, cost in self.car.expenses_dict.items():
                    data_file.write(f"car,{item},{cost}\n")

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
                # This correctly copies the report file (data.txt)
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
