# Deze wordt gebruikt voor de cursus

import tkinter as tk
from tkinter import ttk
import sqlite3



def fetch_data(sqlcommand):
    # Connecten met een database
    # (wordt aangemaakt indien deze niet bestaat)
    conn = sqlite3.connect('dbCrm.db')

    # Maak een cursor aan
    curs = conn.cursor()

    # Maak de tabel aan indien deze nog niet bestaat
    curs.execute(sqlcommand)
    records = curs.fetchall()

    # Wijzigingen commiten
    conn.commit()

    # Connectie sluiten
    conn.close()

    # Retourneer de resultset (records)
    return records

def exec_comnd(sqlcommand, dict):
    # Connecten met een database
    # (wordt aangemaakt indien deze niet bestaat)
    conn = sqlite3.connect('dbCrm.db')

    # Maak een cursor aan
    curs = conn.cursor()

    # Maak de tabel aan indien deze nog niet bestaat
    curs.execute(sqlcommand, dict)

    # Wijzigingen commiten
    conn.commit()

    # Connectie sluiten
    conn.close()


def fillTree():
    data = fetch_data('Select rowid, * from Personen')
    global count
    count = 0
    for record in data:
        my_treeview.insert(parent='',
                           index=tk.END,
                           iid=count,
                           values=(record[0], record[1], record[2], record[3]))
        count += 1


root = tk.Tk()
root.title('Test Treeview')
#root.iconbitmap('')
root.geometry('800x800')

# Add some style
style = ttk.Style()
# Pick a theme
style.theme_use('alt')
# Configure treeview colors
style.configure('Treeview',
                background='#D3D3D3',
                foreground='black',
                rowheight=25,
                fieldbackground='#D3D3D3')
# Change selected color
style.map('Treeview', background=[('selected', '#347083')])

my_treeview = ttk.Treeview(root, show='headings')

# Create striped row tags
my_treeview.tag_configure('oddrow', background='white')
my_treeview.tag_configure('evenrow', background='lightblue')

# Colommen definieren
my_treeview['columns'] = ('ID', 'voornaam', 'achternaam', 'geslacht')

# Format colummen
#my_treeview.column('#0', width=120, minwidth=25)
my_treeview.column('voornaam', anchor='w', width=120)
my_treeview.column('ID', anchor='center', width=80)
my_treeview.column('achternaam', width=120, anchor='w')
my_treeview.column('geslacht', width=100, anchor='w')

# Create headings
#my_treeview.heading('#0', text='Label', anchor='w')
my_treeview.heading('voornaam', text='Voornaam', anchor='w')
my_treeview.heading('ID', text='Id', anchor='center')
my_treeview.heading('achternaam', text='Achternaam', anchor='w')
my_treeview.heading('geslacht', text='Geslacht', anchor='w')



# Data invoegen bij opstarten programma
fillTree()
# my_treeview.insert(parent='', index='end', iid=0, text='Parent1', values=(1, 'John', 'Smith', 'Man'))
# my_treeview.insert(parent='', index='end', iid=1, text='Pietjpuk', values=(2, 'Betsie', 'Jansen', 'Vrouw'))
# my_treeview.insert(parent='1', index='end', iid=2, text='Paulus', values=(1.2, 'Jantine', 'Vulpen', 'Vrouw'))

# Pack
my_treeview.pack(pady=20)

# Add record entry boxes
data_frame = tk.LabelFrame(root, text='Record')
data_frame.pack(fill='x', expand='yes', padx=20)

lblFirstNm = tk.Label(data_frame, text='Voornaam:')
lblFirstNm.grid(row=0, column=0, padx=10, pady=10)
edtFirstNm = tk.Entry(data_frame)
edtFirstNm.grid(row=0, column=1, padx=10, pady=10)

lblLastNm = tk.Label(data_frame, text='Achternaam:')
lblLastNm.grid(row=0, column=2, padx=10, pady=10)
edtLastNm = tk.Entry(data_frame)
edtLastNm.grid(row=0, column=3, padx=10, pady=10)

lblID = tk.Label(data_frame, text='Id:')
lblID.grid(row=1, column=2, padx=10, pady=10)
edtID = tk.Entry(data_frame)
edtID.grid(row=1, column=3, padx=10, pady=10)

lblGeslacht = tk.Label(data_frame, text='Geslacht:')
lblGeslacht.grid(row=1, column=0, padx=10, pady=10)
edtGeslacht = tk.Entry(data_frame)
edtGeslacht.grid(row=1, column=1, padx=10, pady=10)

def clearEdits():
    edtID.delete(0, tk.END)
    edtGeslacht.delete(0, tk.END)
    edtLastNm.delete(0, tk.END)
    edtFirstNm.delete(0, tk.END)


btnClear = tk.Button(data_frame, text='Clear edits', command=clearEdits)
btnClear.grid(row=2, column=0, padx=10, pady=10)

# Add button toevoegen
def toevoegenRec():
    my_treeview.insert(parent='', index='end', iid=len(my_treeview.get_children()) + 1, values=(edtID.get(), edtFirstNm.get(), edtLastNm.get(), edtGeslacht.get()))

    # Record ook aan database toevoegen
    sqlcmnd = '''insert into personen 
    (VoorNm,
    AchterNm,
    Geslacht) 
    Values
    (:voor,
    :achter,
    :geslacht) 
     
    '''
    dict = {'voor': edtFirstNm.get(),
            'achter': edtLastNm.get(),
            'geslacht': edtGeslacht.get()}
    exec_comnd(sqlcmnd, dict)

btnToevoeg = tk.Button(root, text='Toevoegen', command=toevoegenRec)
btnToevoeg.pack(pady=10)

# Een rec wissen
def wisGeselecteerde():
    rec = my_treeview.selection()[0]
    my_treeview.delete(rec)

    # Record ook in database deleten
    sqlcmnd = 'delete from personen where rowid = :id'
    dict = {'id': edtID.get()}
    exec_comnd(sqlcmnd, dict)


btnWisEen = tk.Button(root, text='Wis eerste geselecteerde', command=wisGeselecteerde)
btnWisEen.pack(pady=10)

# Meerdere geselcteerde recs wissen
def wisAlleGeselecteerde():
    recs = my_treeview.selection()
    for rec in recs:
        my_treeview.delete(rec)


# Record selecteren
def selecteerRec(e):
    selectRec()


def selectRec():
    clearEdits()

    # Record nummer ophalen
    selected = my_treeview.focus()
    # Record waarden ophalen
    values = my_treeview.item(selected, 'values')

    # Editboxen vullen met values
    edtID.insert(0, values[0])
    edtGeslacht.insert(0, values[3])
    edtLastNm.insert(0, values[2])
    edtFirstNm.insert(0, values[1])

def refreshData():
    clearEdits()

    # Record nummer ophalen
    selected = my_treeview.focus()
    my_treeview.delete(*my_treeview.get_children())
    fillTree()
    my_treeview.focus(selected)
    my_treeview.selection_set(selected)
    selectRec()


btnRefreshData = tk.Button(root, text='Refresh data', command=refreshData)
btnRefreshData.pack(pady=10)


def updateRec():
    # Record nummer ophalen
    selected = my_treeview.focus()
    # Record opslaan
    values = my_treeview.item(selected, text='', values=(edtID.get(), edtFirstNm.get(), edtLastNm.get(), edtGeslacht.get()))

    # Record in database wijzigen
    sqlcmnd = '''Update personen set
    VoorNm = :voor,
    AchterNm = :achter,
    Geslacht = :geslacht 
    Where rowid = :id 
    '''
    dict = {'voor': edtFirstNm.get(),
            'achter': edtLastNm.get(),
            'geslacht': edtGeslacht.get(),
            'id': edtID.get()}
    exec_comnd(sqlcmnd, dict)


# Treeview en Entryboxen binden
# Hieronder wordt het loslaten van de rechtermuisknop verbonden met functie selecteerRec
my_treeview.bind('<ButtonRelease-1>', selecteerRec)

btnUpdateRec = tk.Button(root, text='Update rec.', command=updateRec)
btnUpdateRec.pack(pady=10)


btnWisEen = tk.Button(root, text='Wis alle geselecteerde', command=wisAlleGeselecteerde)
btnWisEen.pack(pady=10)


root.mainloop()

# '''
#         CREATE TABLE if not exists
#         Personen (
#             VoorNm TEXT,
#             AchterNm TEXT,
#             Geslacht TEXT,
#             IdCode TEXT
#         )
#     '''