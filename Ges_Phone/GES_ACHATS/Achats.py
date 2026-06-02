from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
import re
from subprocess import call
import os


# DB configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'ges_achats',
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def open_menu():
    root.destroy()
    call(["python", os.path.join(os.path.dirname(__file__), 'Menu.py')])


def is_valid_phone(phone):
    if not phone:
        return False
    return bool(re.match(r'^\+?\d[\d\s\-]{6,}$', phone.strip()))


def validate_form(data):
    errors = {}
    if not data['code']:
        errors['code'] = 'Matricule obligatoire'
    if not data['fournisseur']:
        errors['fournisseur'] = 'Fournisseur obligatoire'
    if not data['produit']:
        errors['produit'] = 'Produit obligatoire'
    if not is_valid_phone(data['telephone']):
        errors['telephone'] = 'Téléphone invalide'
    # prix
    try:
        prix = float(str(data['prix']).replace(',', '.'))
        if prix <= 0:
            errors['prix'] = 'Prix doit être > 0'
        else:
            data['prix'] = prix
    except Exception:
        errors['prix'] = 'Prix invalide'
    # quantite
    try:
        qte = int(float(data['quantite']))
        if qte <= 0:
            errors['quantite'] = 'Quantité doit être > 0'
        else:
            data['quantite'] = qte
    except Exception:
        errors['quantite'] = 'Quantité invalide'

    return errors, data


def get_form_data():
    return {
        'code': txtCode.get().strip(),
        'fournisseur': txtFournisseur.get().strip(),
        'telephone': txtTel.get().strip(),
        'produit': cbProduit.get().strip(),
        'prix': txtPrix.get().strip(),
        'quantite': txtQte.get().strip(),
    }


def clear_form():
    txtCode.delete(0, END)
    txtFournisseur.delete(0, END)
    txtTel.delete(0, END)
    txtPrix.delete(0, END)
    txtQte.delete(0, END)
    cbProduit.set('')
    txtCode.focus()


def load_data():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT code, fournisseur, telephone, produit, prix, quantite FROM tb_achat ORDER BY code')
        rows = cur.fetchall()
    except Exception as e:
        messagebox.showerror('Erreur', str(e))
        return
    finally:
        try:
            conn.close()
        except Exception:
            pass

    table.delete(*table.get_children())
    for row in rows:
        try:
            prix_val = float(row[4])
            prix_display = f"{prix_val:.2f} francs"
        except Exception:
            prix_display = f"{row[4]} francs"
        display_row = (row[0], row[1], row[2], row[3], prix_display, row[5])
        table.insert('', END, values=display_row)


def select_row(event):
    item = table.focus()
    if not item:
        return
    values = table.item(item, 'values')
    clear_form()
    txtCode.insert(0, values[0])
    txtFournisseur.insert(0, values[1])
    txtTel.insert(0, values[2])
    cbProduit.set(values[3])
    prix_display = values[4]
    m = re.search(r'[-\d.,]+', str(prix_display))
    if m:
        prix_num = m.group(0).replace(',', '.')
    else:
        prix_num = str(prix_display)
    txtPrix.insert(0, prix_num)
    txtQte.insert(0, values[5])


def add():
    data = get_form_data()
    errors, data = validate_form(data)
    if errors:
        messagebox.showerror('Erreur', '\n'.join([f"{k}: {v}" for k, v in errors.items()]))
        first = next(iter(errors))
        focus_map = {'code': txtCode, 'fournisseur': txtFournisseur, 'telephone': txtTel, 'produit': cbProduit, 'prix': txtPrix, 'quantite': txtQte}
        try:
            focus_map[first].focus_set()
        except Exception:
            pass
        return

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT 1 FROM tb_achat WHERE code=%s', (data['code'],))
        if cur.fetchone():
            messagebox.showwarning('Attention', 'Code déjà utilisé')
            return
        cur.execute('INSERT INTO tb_achat (code, fournisseur, telephone, produit, prix, quantite) VALUES (%s,%s,%s,%s,%s,%s)',
                    (data['code'], data['fournisseur'], data['telephone'], data['produit'], data['prix'], data['quantite']))
        conn.commit()
    except Exception as e:
        messagebox.showerror('Erreur', str(e))
        return
    finally:
        try:
            conn.close()
        except Exception:
            pass

    messagebox.showinfo('Succès', 'Ajout réussi')
    clear_form()
    load_data()


def update():
    data = get_form_data()
    if not data['code']:
        messagebox.showerror('Erreur', 'Code obligatoire')
        return
    errors, data = validate_form(data)
    if errors:
        messagebox.showerror('Erreur', '\n'.join([f"{k}: {v}" for k, v in errors.items()]))
        return
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('UPDATE tb_achat SET fournisseur=%s, telephone=%s, produit=%s, prix=%s, quantite=%s WHERE code=%s',
                    (data['fournisseur'], data['telephone'], data['produit'], data['prix'], data['quantite'], data['code']))
        conn.commit()
    except Exception as e:
        messagebox.showerror('Erreur', str(e))
        return
    finally:
        try:
            conn.close()
        except Exception:
            pass
    messagebox.showinfo('Succès', 'Modification réussie')
    load_data()


def delete():
    code = txtCode.get().strip()
    if not code:
        messagebox.showerror('Erreur', 'Code obligatoire')
        return
    if not messagebox.askyesno('Confirmation', 'Supprimer cet achat ?'):
        return
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM tb_achat WHERE code=%s', (code,))
        conn.commit()
    except Exception as e:
        messagebox.showerror('Erreur', str(e))
        return
    finally:
        try:
            conn.close()
        except Exception:
            pass
    messagebox.showinfo('Succès', 'Suppression réussie')
    clear_form()
    load_data()


# =========================
# UI - Menu style
# =========================
def on_enter(e):
    e.widget.config(cursor='hand2')


def on_leave(e):
    e.widget.config(cursor='')


root = Tk()
root.title('Gestion des Achats')
root.geometry('1200x700')
root.resizable(True, True)
root.configure(bg='#0F172A')

# center window
largeur = 1200
hauteur = 700
x = (root.winfo_screenwidth() // 2) - (largeur // 2)
y = (root.winfo_screenheight() // 2) - (hauteur // 2)
root.geometry(f"{largeur}x{hauteur}+{x}+{y}")

# Header
header = Frame(root, bg='#1E293B', height=90)
header.pack(fill=X)
Label(header, text='GESTION DES ACHATS', font=('Segoe UI', 28, 'bold'), fg='white', bg='#1E293B').pack(pady=20)

Label(root, text='MENU ACHATS', font=('Segoe UI', 20, 'bold'), bg='#0F172A', fg='white').pack()
Label(root, text="Gérer les achats (ajout / modification / suppression)", font=('Segoe UI', 11), bg='#0F172A', fg='#94A3B8').pack(pady=5)

# Form and table layout
frame_main = Frame(root, bg='#0F172A')
frame_main.pack(fill=BOTH, expand=True, padx=20, pady=10)

left = Frame(frame_main, bg='#0F172A')
left.pack(side=LEFT, fill=Y, padx=(0, 20))

right = Frame(frame_main, bg='#0F172A')
right.pack(side=RIGHT, fill=BOTH, expand=True)

# Inputs
Label(left, text='MATRICULE', bg='#0F172A', fg='white', font=('Segoe UI', 12, 'bold')).grid(row=0, column=0, sticky=W, pady=8)
txtCode = Entry(left, bg='#0b1220', fg='white', bd=0, width=28)
txtCode.grid(row=0, column=1, pady=8)

Label(left, text='FOURNISSEURS', bg='#0F172A', fg='white', font=('Segoe UI', 12, 'bold')).grid(row=1, column=0, sticky=W, pady=8)
txtFournisseur = Entry(left, bg='#0b1220', fg='white', bd=0, width=28)
txtFournisseur.grid(row=1, column=1, pady=8)

Label(left, text='TELEPHONE', bg='#0F172A', fg='white', font=('Segoe UI', 12, 'bold')).grid(row=2, column=0, sticky=W, pady=8)
txtTel = Entry(left, bg='#0b1220', fg='white', bd=0, width=28)
txtTel.grid(row=2, column=1, pady=8)

Label(left, text='PRODUIT', bg='#0F172A', fg='white', font=('Segoe UI', 12, 'bold')).grid(row=3, column=0, sticky=W, pady=8)
cbProduit = ttk.Combobox(left, values=['IPHONE 12', 'IPHONE 11', 'GALAXY S22', 'XIAOMI', 'S10', 'HAQUEI', 'PRO 64', 'NOKIA', 'AUTRES'], width=26)
cbProduit.grid(row=3, column=1, pady=8)

Label(left, text='PRIX', bg='#0F172A', fg='white', font=('Segoe UI', 12, 'bold')).grid(row=4, column=0, sticky=W, pady=8)
txtPrix = Entry(left, bg='#0b1220', fg='white', bd=0, width=20)
txtPrix.grid(row=4, column=1, pady=8, sticky=W)
Label(left, text='francs', bg='#0F172A', fg='#94A3B8', font=('Segoe UI', 10)).grid(row=4, column=1, sticky=E)

Label(left, text='QUANTITE', bg='#0F172A', fg='white', font=('Segoe UI', 12, 'bold')).grid(row=5, column=0, sticky=W, pady=8)
txtQte = Entry(left, bg='#0b1220', fg='white', bd=0, width=28)
txtQte.grid(row=5, column=1, pady=8)

# Buttons
frame_btns = Frame(left, bg='#0F172A')
frame_btns.grid(row=6, column=0, columnspan=2, pady=12)
btn_enregistrer = Button(frame_btns, text='ENREGISTRER', bg='#10B981', fg='white', font=('Segoe UI', 11, 'bold'), bd=0, padx=12, pady=8, command=add)
btn_enregistrer.grid(row=0, column=0, padx=6)
btn_modifier = Button(frame_btns, text='MODIFIER', bg='#3B82F6', fg='white', font=('Segoe UI', 11, 'bold'), bd=0, padx=12, pady=8, command=update)
btn_modifier.grid(row=0, column=1, padx=6)
btn_supprimer = Button(frame_btns, text='SUPPRIMER', bg='#F59E0B', fg='white', font=('Segoe UI', 11, 'bold'), bd=0, padx=12, pady=8, command=delete)
btn_supprimer.grid(row=0, column=2, padx=6)
btn_retour = Button(frame_btns, text='RETOUR', bg='#EF4444', fg='white', font=('Segoe UI', 11, 'bold'), bd=0, padx=12, pady=8, command=open_menu)
btn_retour.grid(row=0, column=3, padx=6)

for b in [btn_enregistrer, btn_modifier, btn_supprimer, btn_retour]:
    b.bind('<Enter>', on_enter)
    b.bind('<Leave>', on_leave)

# Table
cols = ('code', 'fournisseur', 'telephone', 'produit', 'prix', 'quantite')
table = ttk.Treeview(right, columns=cols, show='headings')
for c in cols:
    table.heading(c, text=c.upper())

vsb = Scrollbar(right, orient=VERTICAL, command=table.yview)
table.configure(yscroll=vsb.set)
vsb.pack(side=RIGHT, fill=Y)
table.pack(fill=BOTH, expand=True)

table.column('code', width=120)
table.column('fournisseur', width=200)
table.column('telephone', width=140)
table.column('produit', width=180)
table.column('prix', width=140, anchor=E)
table.column('quantite', width=100, anchor=E)

table.bind('<<TreeviewSelect>>', select_row)

load_data()

# Footer
footer = Label(root, text='© 2026 - Application de Gestion Commerciale', font=('Segoe UI', 10), bg='#0F172A', fg='#64748B')
footer.pack(side=BOTTOM, pady=12)

root.mainloop()