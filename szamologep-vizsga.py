import tkinter as tk

# Főablak létrehozása
root = tk.Tk()
root.title("Grafikus Számológép")

# Kijelző létrehozása
display = tk.Entry(root, font=("Arial", 20), justify="right")
display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipadx=10, ipady=10)

# Gombok szövegei
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+'
]

# Gombok eseménykezelője
def button_click(value):
    if value == "=":
        try:
            result = eval(display.get())
            display.delete(0, tk.END)
            display.insert(tk.END, str(result))
        except Exception as e:
            display.delete(0, tk.END)
            display.insert(tk.END, "Hiba")
    else:
        display.insert(tk.END, value)

# Gombok létrehozása és elhelyezése
row = 1
col = 0
for button in buttons:
    tk.Button(root, text=button, font=("Arial", 15), width=5, height=2,
              command=lambda b=button: button_click(b)).grid(row=row, column=col, padx=5, pady=5)
    col += 1
    if col > 3:
        col = 0
        row += 1

# Törlés gomb
tk.Button(root, text="C", font=("Arial", 15), width=5, height=2,
          command=lambda: display.delete(0, tk.END)).grid(row=row, column=col, padx=5, pady=5)

# Főciklus indítása
root.mainloop()
