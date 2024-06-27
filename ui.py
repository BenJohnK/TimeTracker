import tkinter as tk
from tkinter import ttk

def on_save_button_click(*args):
    if "disabled" in save_button["state"]:
        if not expanded:
            toggle_text_area()

def click(event=None):
    current_text = token_input.get()
    if current_text == "Please enter your token":
        token_input.delete(0, 'end') 

def enable_save_button():
    current_text = token_input.get()
    if current_text and current_text != "Please enter your token":
        save_button.config(state="normal")
    else:
        save_button.config(state="disabled")
        # if not expanded:  # Check if the text area is not already expanded
        #     toggle_text_area()

def on_submit():
    token = token_input.get()
    print(token)
    root.destroy()

# call function when we leave entry box 
def leave(*args):
    if not token_input.get():
      token_input.insert(0, 'Please enter your token')
    root.focus()

def toggle_text_area():
    global expanded
    if expanded:
        token_input.grid_forget()  # Hide the text area
        bottom_line.grid_forget()
        expand_button.config(image=expand_icon)
        expanded = False
    else:
        token_input.grid(row=0, column=0, padx=40, pady=145, sticky="nw")
        bottom_line.grid(row=0, column=0, padx=40, pady=165, sticky="nw")
        if not token_input.get():  # Check if entry is empty
            token_input.insert(0, 'Please enter your token')
        expand_button.config(image=collapse_icon)
        expanded = True

def close_window():
    root.destroy()

root = tk.Tk()

# root.overrideredirect(True)

root.geometry("700x200")
root.config(bg="white")
root.resizable(False, False)

  # Replace "image.png" with the path to your image
image = tk.PhotoImage(file="logo.png")

close_icon = tk.PhotoImage(file="close-icon-2.png")
expand_icon = tk.PhotoImage(file="play-button.png")
collapse_icon = tk.PhotoImage(file="collapse-button.png")

subsample_x = 2  # Scale factor for the width
subsample_y = 2  # Scale factor for the height
scaled_image = image.subsample(subsample_x, subsample_y)

frame = tk.Frame(root, highlightbackground="silver", highlightthickness=0.5, bg="white")
frame.pack(fill="both", expand=True, padx=8, pady=5)

image_label = tk.Label(frame, image=scaled_image, bg="white")
image_label.grid(row=0, column=0, padx=20, pady=10, sticky="nw")

close_label = tk.Label(frame, image=close_icon, bg="white", cursor="hand2")
close_label.grid(row=0, column=0, padx=640, pady=20, sticky="nw")

close_label.bind("<Button-1>", lambda event: close_window())

expand_button = tk.Button(frame, image=expand_icon, bg="white", cursor="hand2", command=toggle_text_area, borderwidth=0, highlightthickness=0)
expand_button.grid(row=0, column=0, padx=30, pady=100, sticky="nw")

auth_label = tk.Label(frame, text="Authentication Vault", bg="white", font=("Arial", 13))
auth_label.grid(row=0, column=0, padx=50, pady=97, sticky="nw")

style = ttk.Style()
style.configure("Save.TButton", background="#1d90ff", foreground="white", borderwidth=0, highlightthickness=0, padding=10)


token_input = tk.Entry(frame, width=60, borderwidth=0, highlightthickness=0)
token_input.bind("<FocusIn>", click)
token_input.bind("<Leave>", leave)
token_input.bind("<KeyRelease>", lambda event: enable_save_button())
expanded = False

save_button = tk.Button(frame, text="SAVE", background="#1d90ff", foreground="white", command=on_submit, cursor="hand2", highlightthickness=0, borderwidth=0, activebackground="#1d90ff", activeforeground="white", font=('Arial', 15), padx=55, pady=10, disabledforeground="silver")
save_button.grid(row=0, column=0, padx=500, pady=110, sticky="nw")
bottom_line = tk.Frame(frame, height=1,width=200, bg="black")
enable_save_button()

save_button.bind("<Button-1>", on_save_button_click)

root.mainloop()