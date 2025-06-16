import tkinter as tk
from tkinter import ttk

from .main import load_recalls, load_purchases, check_recalls


def run_gui():
    def on_check():
        recalls = load_recalls()
        purchases = load_purchases()
        alerts = check_recalls(recalls, purchases)
        listbox.delete(0, tk.END)
        if alerts:
            status_var.set("Produits rappelés trouvés :")
            for item in alerts:
                listbox.insert(tk.END, f"{item['name']} ({item['brand']})")
        else:
            status_var.set("Aucun produit rappelé parmi vos achats.")

    root = tk.Tk()
    root.title("RecallMe")

    ttk.Label(root, text="Vérifiez vos achats par rapport aux rappels de produits").pack(pady=10)
    ttk.Button(root, text="Vérifier", command=on_check).pack()

    status_var = tk.StringVar()
    ttk.Label(root, textvariable=status_var).pack(pady=10)

    listbox = tk.Listbox(root, width=40)
    listbox.pack(padx=10, pady=5)

    root.mainloop()


if __name__ == "__main__":
    run_gui()
