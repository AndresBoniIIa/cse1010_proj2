class Budget:
    def __init__(self, expense_type):
        self.expense_type = expense_type
        self.expenses = []
        #self.catas = []
        self.expenses_dict = {}
    
    def add_expenses(self):
        while True:   
            try:
                num_expenses = int(input(f"How many {self.expense_type} expenses do you want to enter? "))
                break
            except:
                print("** ERROR: Wrong Input **")
                print()
        example = "Oil 10" if self.expense_type.lower() == "car" else "Milk 10"
        print(f"Enter expenses in \"Type Cost\" format. for e.g., {example} ")
        for i in range(num_expenses):
            while True:
                try:
                    type, exp = input(f"Enter expenses #{i+1}: ").split()
                    self.expenses_dict[type] = float(exp)
                    #self.expenses.append(float(exp))
                    #self.catas.append(type)
                    break
                except:
                    print()
                    print("ERROR: WRONG INPUT FORMAT")
                    print()
        self.write_to_file()


    def get_expenses(self):
        total = sum(self.expenses)
        print(f"Total money you spent on {self.expense_type} is ${sum(self.expenses_dict.values())}")
        return sum(self.expenses_dict.values())

    def get_expenses_list(self):
        print()
        print(f"List of {self.expense_type} expenses")

        for type, exp in self.expense_dict.items():
            print(f"{type} : ${exp}")
    
    def write_to_file(self):
        with open("data.txt", "a") as data:
            data.write(self.expense_type)
            data.write("\n")
            for type, exp in self.expenses_dict.item():
                data.write(f"{type} : ${exp}")
                data.write("\n")
            data.write("\n")
