def calc_balance(income, expenses):
    balance = income - expenses
    print(f"Your monthly income from the data you provided me is: ${balance}")
    return balance

def finacial_status(balance):

    if (balance > 0):
        print("Great! You are saving money!")
    elif (balance == 0):
        print("You are breaking even.")
    elif (balance < 0):
        print("**WARNING** You are overspending!")
