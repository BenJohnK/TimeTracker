import tkinter as tk
from tkinter import messagebox
import requests

def call_api(number1, number2):
    url = f'https://api.example.com/add?num1={number1}&num2={number2}'

    try:
        response = requests.get(url)
        result = response.json()

        # Display the API result
        messagebox.showinfo("API Result", f"The sum is: {result['sum']}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def on_submit():
    try:
        # Get numbers from entry widgets
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())

        # Call the API with the provided numbers
        call_api(num1, num2)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

# Create the main window
root = tk.Tk()
root.title("API Caller")

# Create and place entry widgets
label_num1 = tk.Label(root, text="Number 1:")
label_num1.grid(row=0, column=0, padx=10, pady=10)

entry_num1 = tk.Entry(root)
entry_num1.grid(row=0, column=1, padx=10, pady=10)

label_num2 = tk.Label(root, text="Number 2:")
label_num2.grid(row=1, column=0, padx=10, pady=10)

entry_num2 = tk.Entry(root)
entry_num2.grid(row=1, column=1, padx=10, pady=10)

# Create and place submit button
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.grid(row=2, column=0, columnspan=2, pady=10)

# Run the Tkinter event loop
root.mainloop()