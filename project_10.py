import os 
from Library import functions 
from Library.classes_9 import Budget

os.system('cls' if os.name == 'nt' else 'clear')
name = input("Enter your name: ")
os.system('cls' if os.name == 'nt' else 'clear')
 

print(f"hey {name}, this is BudgetBuddy! your personal budgeting assistant")
income_monthly = float(input("Please state your monthly income: "))

total_expenses = []
grocery = Budget("grocery")
car = Budget("car")

grocery.add_expenses()
car.add_expenses()

total_expenses.append(grocery.get_expenses())
total_expenses.append(car.get_expenses())
   
bal = functions.calc_balance(income_monthly, sum(total_expenses))
functions.finacial_status(bal)

print()
grocery.get_expenses_list()
print()
car.get_expenses_list()
