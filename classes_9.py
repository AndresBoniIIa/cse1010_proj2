class Budget: 
    def __init__(self, expense_type):
        self.expense_type = expense_type
        self.category = [] 
        self.expenses = []

    def add_expenses(self): 
        print(f"\n--- Adding Expenses for: {self.expense_type} ---")
        print("Type 'done' when you are finished.")
        
        while True:
            user_input = input(f"Enter expense (e.g., Milk $10, Car Repair $200): ").strip()

            if user_input.lower() == 'done':
                break 
                print("All expenses recorded successfully.")

            
            try:
                parts = user_input.split()

                if len(parts) < 2:
                    raise ValueError("Invalid format.")

                cost = float(parts[-1]) 
                item = " ".join(parts[:-1])
                
                self.category.append(item)
                self.expenses.append(cost)
                print(f"  > Added: {item}, ${cost:.2f}")

            except ValueError:
                print(f"  > Error: Invalid input. Please use 'Item Cost' format. Try again.")

    def get_expenses(self):
       print(f"Total money you spent on {self.expense_type} is {sum(self.expenses)}.")
       return sum(self.expenses)

    def get_expense_details(self):
        print(f"\n--- Itemized List for {self.expense_type} ---")
        
        if not self.category:
            print("  No expenses entered for this category.")
            return

        for item, cost in zip(self.category, self.expenses):
            print(f"  - {item}: ${cost:.2f}")
