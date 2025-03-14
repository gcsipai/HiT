import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import os

def zip_files():
    # Fájlok kiválasztása
    file_paths = filedialog.askopenfilenames(title="Válaszd ki a tömörítendő fájlokat")
    if not file_paths:
        messagebox.showwarning("Figyelem", "Nincsenek kiválasztva fájlok!")
        return

    # ZIP fájl mentési helyének kiválasztása
    zip_path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP fájlok", "*.zip")])
    if not zip_path:
        messagebox.showwarning("Figyelem", "Nincs kiválasztva mentési hely!")
        return

    try:
        # ZIP fájl létrehozása és fájlok hozzáadása
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in file_paths:
                zipf.write(file, os.path.basename(file))
        messagebox.showinfo("Siker", "A fájlok sikeresen tömörítve lettek!")
    except Exception as e:
        messagebox.showerror("Hiba", f"Hiba történt a tömörítés során: {e}")

# Grafikus felület létrehozása
root = tk.Tk()
root.title("ZIP Tömörítő")

# Címke
label = tk.Label(root, text="Válaszd ki a tömörítendő fájlokat, majd a mentési helyet")
label.pack(pady=10)

# Tömörítés gomb
zip_button = tk.Button(root, text="Fájlok tömörítése", command=zip_files)
zip_button.pack(pady=20)

# Főciklus indítása
root.mainloop()
