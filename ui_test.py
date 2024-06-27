import tkinter as tk
from PIL import Image
from PIL import ImageTk

def show_entry_box():
  # Create the entry field and label within the main window
  global entry, label  # Declare these variables globally for access

  label = tk.Label(root, text="Enter Token:")
  label.grid(row=2, column=0, padx=5, pady=5)

  entry = tk.Entry(root)
  entry.grid(row=2, column=1, padx=5, pady=5)

  # Create a button to submit the token
  submit_button = tk.Button(root, text="Submit", command=lambda: handle_token_submission(entry.get()))
  submit_button.grid(row=3, columnspan=2, padx=5, pady=5)

  # Hide the entry field and label initially
  label.grid_remove()
  entry.grid_remove()
  submit_button.grid_remove()

def handle_token_submission(token):
  global submit_button
  # Process the entered token here (e.g., store it or validate it)
  print(f"Token entered: {token}")

  # Hide the entry field and button after submission
  label.grid_remove()
  entry.grid_remove()
  submit_button.grid_remove()

# Create the main window
root = tk.Tk()
root.title("Authentication Vault")



# Add your logo image (replace "logo.png" with your actual image path)
logo_image = tk.PhotoImage(file="logo.png")
logo_label = tk.Label(root, image=logo_image)
logo_label.grid(row=0, columnspan=2, pady=10)  # Adjust padding as needed

# Create the close button
close_button = tk.Button(root, text="X", font=("Arial", 16), command=root.destroy)
close_button.grid(row=1, column=1, sticky="ne", padx=5, pady=5)

width = 10
height = 10
img = Image.open("play-button-arrowhead.png")
img = img.resize((width,height), Image.Resampling.LANCZOS)
photoImg =  ImageTk.PhotoImage(img)
# Create the down arrow button

down_arrow_button = tk.Button(root, image=photoImg, command=show_entry_box)
down_arrow_button.grid(row=1, column=0, sticky="nw", padx=5, pady=5)

# Initialize the entry field and label as hidden (using grid_remove())
entry = None
label = None

# Run the main event loop
root.mainloop()