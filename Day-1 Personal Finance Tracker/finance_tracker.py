#Collect Income
from xml.etree.ElementTree import TreeBuilder


def get_income():
    while True:
        try:
            income = float(input("Enter your monthly income: $"))
            if income <= 0:
                print("Income must be positive.")
                continue
            return income
        except ValueError:
            print("Please enter a valid number.")

#Collect Expenses by category
def get_expenses():
    categories = ["Rent","Food","Transport","Savings","Entertainment","Other"] # type: ignore
    expenses = {} # type: ignore

    print("\nEnter your monthly expenses (enter 0 to skip):")
    for category in categories:
        while True:
            try:
                amount = float(input(f"  {category}: $"))
                if amount <0:
                    print("Amount can't be negative.")
                    continue
                expenses[category] = amount
                break
            except ValueError:
                print("Please enter a valid number.")
    return expenses 

#Analysis Function 
def calculate_summary(income, expenses):
    total_spent = sum(expenses.values())
    savings = income - total_spent
    savings_rate = (savings/income) *100

    top_category = max(expenses, key=lambda cat:expenses[cat])
    top_percentage = (expenses[top_category]/ income)*100

    return {
        "total_spent":total_spent,
        "savings":savings,
        "savings_rate":savings_rate,
        "top_category":top_category,
        "top_percentage":top_percentage
    }


#Print the Report
def print_finance_report(income,expenses, summary):
    print("\n" + "="*45)
    print("   PERSONAL FINANCE REPORT   ")
    print("="*45)
    print(f"Monthly Income :${income:,.2f}")
    print(f"Total Expenses :${summary['total_spent']:,.2f}")
    print(f"Net Savings: ${summary['savings']:,.2f}")
    print(f"Savings Rate: {summary['savings_rate']:.1f}%")
    print(f"\nTop Spending Category: {summary['top_category']}"
          f"({summary['top_percentage']:.1f}% of income)")
    
    print("\n---Expense Breakdown---")
    for category, amount in expenses.items():
        if amount>0:
            pct = (amount/income)*100
            bar ="#" * int(pct/5)
            print(f"{category:<14}:${amount:>8,.2f} {bar} {pct:.1f}%")
    print("=" *45)


# Main Runnner
def main():
    print("Personal Finance Tracker")
    print("-"*30)
    income = get_income()
    expenses = get_expenses()
    summary = calculate_summary(income,expenses)
    print_finance_report(income,expenses,summary)
    
#function call
main()