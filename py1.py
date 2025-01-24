import tkinter as tk
from tkinter import ttk
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import messagebox as mb


transactions = []
budget = 0  


def add_transaction():
    def save_transaction():
        try:
            amount = float(amount_entry.get())
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")

            category = category_entry.get().strip()
            if not category:
                raise ValueError("Category cannot be empty.")

            type_ = type_combobox.get()
            if type_ not in ["Income", "Expense"]:
                raise ValueError("Please select a valid type.")

            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            transaction = {
                "amount": amount,
                "category": category,
                "type": type_,
                "date": date
            }
            transactions.append(transaction)
            status_label.config(text="Transaction added successfully!", fg="green")
            add_window.destroy()
        except ValueError as e:
            mb.showerror("Input Error", str(e))

    add_window = tk.Toplevel(root)
    add_window.title("Add Transaction")
    add_window.geometry("300x200")

    tk.Label(add_window, text="Amount:").grid(row=0, column=0, pady=5, padx=5, sticky="w")
    amount_entry = tk.Entry(add_window)
    amount_entry.grid(row=0, column=1, pady=5, padx=5)

    tk.Label(add_window, text="Category:").grid(row=1, column=0, pady=5, padx=5, sticky="w")
    category_entry = tk.Entry(add_window)
    category_entry.grid(row=1, column=1, pady=5, padx=5)

    tk.Label(add_window, text="Type:").grid(row=2, column=0, pady=5, padx=5, sticky="w")
    type_combobox = ttk.Combobox(add_window, values=["Income", "Expense"])
    type_combobox.grid(row=2, column=1, pady=5, padx=5)

    save_button = tk.Button(add_window, text="Save", command=save_transaction)
    save_button.grid(row=3, column=0, columnspan=2, pady=10)


def view_transactions():
    view_window = tk.Toplevel(root)
    view_window.title("View Transactions")
    view_window.geometry("500x300")  

    if not transactions:
        tk.Label(view_window, text="No transactions found.", fg="red").pack(pady=10)
        return

    tree = ttk.Treeview(view_window, columns=("Amount", "Category", "Type", "Date"), show="headings")
    tree.heading("Amount", text="Amount")
    tree.heading("Category", text="Category")
    tree.heading("Type", text="Type")
    tree.heading("Date", text="Date")

    # Set column widths
    tree.column("Amount", width=100)
    tree.column("Category", width=120)
    tree.column("Type", width=80)
    tree.column("Date", width=150)  # Increased width for date column

    for transaction in transactions:
        tree.insert("", "end", values=(transaction["amount"], transaction["category"], transaction["type"], transaction["date"]))

    tree.pack(fill="both", expand=True)

# Function to visualize spending by category
def visualize_spending():
    categories = {}
    for transaction in transactions:
        if transaction["type"] == "Expense":
            categories[transaction["category"]] = categories.get(transaction["category"], 0) + transaction["amount"]

    if not categories:
        mb.showinfo("No Data", "No expense data available to visualize.")
        return

    labels = list(categories.keys())
    sizes = list(categories.values())

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    ax.set_title("Spending by Category")

    # Embed the plot in the Tkinter window
    plot_window = tk.Toplevel(root)
    plot_window.title("Spending Visualization")
    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# Function to set a budget
def set_budget():
    def save_budget():
        global budget
        try:
            budget = float(budget_entry.get())
            if budget <= 0:
                raise ValueError("Budget must be greater than zero.")
            mb.showinfo("Success", f"Budget set to {budget:.2f}.")
            budget_window.destroy()
        except ValueError as e:
            mb.showerror("Input Error", str(e))

    budget_window = tk.Toplevel(root)
    budget_window.title("Set Budget")
    budget_window.geometry("300x100")

    tk.Label(budget_window, text="Enter your budget:").grid(row=0, column=0, pady=5, padx=5)
    budget_entry = tk.Entry(budget_window)
    budget_entry.grid(row=0, column=1, pady=5, padx=5)

    save_button = tk.Button(budget_window, text="Save", command=save_budget)
    save_button.grid(row=1, column=0, columnspan=2, pady=10)

# Function to check budget
def check_budget():
    total_expenses = sum(t["amount"] for t in transactions if t["type"] == "Expense")
    if budget and total_expenses > budget:
        mb.showwarning("Budget Exceeded", f"Your expenses ({total_expenses:.2f}) have exceeded your budget ({budget:.2f})!")
    elif budget:
        mb.showinfo("Budget Status", f"Your total expenses are {total_expenses:.2f}. You are within your budget of {budget:.2f}.")
    else:
        mb.showinfo("No Budget", "No budget set. Please set a budget.")

# Main application window
root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("400x300")

# Widgets in the main window
tk.Label(root, text="Personal Finance Tracker", font=("Arial", 16)).pack(pady=10)

add_button = tk.Button(root, text="Add Transaction", command=add_transaction, width=20)
add_button.pack(pady=5)

view_button = tk.Button(root, text="View Transactions", command=view_transactions, width=20)
view_button.pack(pady=5)

visualize_button = tk.Button(root, text="Visualize Spending", command=visualize_spending, width=20)
visualize_button.pack(pady=5)

budget_button = tk.Button(root, text="Set Budget", command=set_budget, width=20)
budget_button.pack(pady=5)

check_budget_button = tk.Button(root, text="Check Budget", command=check_budget, width=20)
check_budget_button.pack(pady=5)

status_label = tk.Label(root, text="", font=("Arial", 10))
status_label.pack(pady=5)

exit_button = tk.Button(root, text="Exit", command=root.destroy, width=20)
exit_button.pack(pady=5)

root.mainloop()
