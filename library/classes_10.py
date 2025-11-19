class Expense:
    def __init__(self, name: str, cost: float):
        self.name = name
        self.cost = cost

class Category:
    def __init__(self, name: str):
        self.name = name
        self.expenses_dict = {}  # key: expense name, value: Expense object

    def add_expense(self, name, cost):
        self.expenses_dict[name] = Expense(name, cost)

    def edit_expense(self, name, new_cost):
        if name in self.expenses_dict:
            self.expenses_dict[name].cost = new_cost

    def delete_expense(self, name):
        if name in self.expenses_dict:
            del self.expenses_dict[name]

    def total_cost(self):
        return sum(e.cost for e in self.expenses_dict.values())
