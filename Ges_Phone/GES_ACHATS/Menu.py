from tkinter import *
from subprocess import call
import os

# ==========================
# FONCTIONS
# ==========================

def ouvrir_clients():
    root.destroy()
    chemin = os.path.join(os.path.dirname(__file__), "Clients.py")
    call(["python", chemin])

def ouvrir_achats():
    root.destroy()
    chemin = os.path.join(os.path.dirname(__file__), "Achats.py")
    call(["python", chemin])

def ouvrir_ventes():
    root.destroy()
    chemin = os.path.join(os.path.dirname(__file__), "Ventes.py")
    call(["python", chemin])

def quitter():
    root.destroy()


# ==========================
# EFFET SURVOL
# ==========================

def on_enter(e):
    e.widget.config(cursor="hand2")

def on_leave(e):
    e.widget.config(cursor="")


# ==========================
# FENETRE
# ==========================

root = Tk()
root.title("Gestion Commerciale")
root.geometry("1200x700")
root.configure(bg="#0F172A")
root.resizable(True, True)

# Centrer la fenêtre
largeur = 1200
hauteur = 700

x = (root.winfo_screenwidth() // 2) - (largeur // 2)
y = (root.winfo_screenheight() // 2) - (hauteur // 2)

root.geometry(f"{largeur}x{hauteur}+{x}+{y}")

# ==========================
# HEADER
# ==========================

header = Frame(root, bg="#1E293B", height=90)
header.pack(fill=X)

Label(
    header,
    text="GESTION COMMERCIALE",
    font=("Segoe UI", 28, "bold"),
    fg="white",
    bg="#1E293B"
).pack(pady=20)

# ==========================
# LOGO
# ==========================

# Logo removed as requested (no emoji)

Label(
    root,
    text="MENU PRINCIPAL",
    font=("Segoe UI", 20, "bold"),
    bg="#0F172A",
    fg="white"
).pack()

Label(
    root,
    text="Sélectionnez un module pour continuer",
    font=("Segoe UI", 11),
    bg="#0F172A",
    fg="#94A3B8"
).pack(pady=5)

# ==========================
# CONTENEUR BOUTONS
# ==========================

frame_btn = Frame(root, bg="#0F172A")
frame_btn.pack(pady=50)

btn_clients = Button(
    frame_btn,
    text="CLIENTS",
    font=("Segoe UI", 14, "bold"),
    bg="#10B981",
    fg="white",
    width=18,
    height=3,
    bd=0,
    command=ouvrir_clients
)
btn_clients.grid(row=0, column=0, padx=20)

btn_achats = Button(
    frame_btn,
    text="ACHATS",
    font=("Segoe UI", 14, "bold"),
    bg="#3B82F6",
    fg="white",
    width=18,
    height=3,
    bd=0,
    command=ouvrir_achats
)
btn_achats.grid(row=0, column=1, padx=20)

btn_ventes = Button(
    frame_btn,
    text="VENTES",
    font=("Segoe UI", 14, "bold"),
    bg="#F59E0B",
    fg="white",
    width=18,
    height=3,
    bd=0,
    command=ouvrir_ventes
)
btn_ventes.grid(row=0, column=2, padx=20)

btn_quitter = Button(
    frame_btn,
    text="QUITTER",
    font=("Segoe UI", 14, "bold"),
    bg="#EF4444",
    fg="white",
    width=18,
    height=3,
    bd=0,
    command=quitter
)
btn_quitter.grid(row=0, column=3, padx=20)

# Effets de survol
for btn in [btn_clients, btn_achats, btn_ventes, btn_quitter]:
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# ==========================
# FOOTER
# ==========================

footer = Label(
    root,
    text="© 2026 - Application de Gestion Commerciale",
    font=("Segoe UI", 10),
    bg="#0F172A",
    fg="#64748B"
)

footer.pack(side=BOTTOM, pady=20)

# ==========================
# EXECUTION
# ==========================

root.mainloop()