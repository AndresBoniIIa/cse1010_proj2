def calc_balance(income, total_expenses):
    return income - total_expenses

def status(balance):
    if balance > 0:
        return "Great! You are saving money!"
    elif balance == 0:
        return "You are breaking even."
    else:
        return "**WARNING** You are overspending!"
