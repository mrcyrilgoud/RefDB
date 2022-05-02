#Importing Tkinter - Python GUI library

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox
import os

# Importing sqlite3
import sqlite3

# Create the 'ProteinSequence.db' file
connect = sqlite3.connect('ProteinSequence.db')
c = connect.cursor()

#the Tkinter root window
#First window that the user will see
root = tkinter.Tk()

#Specifies basic aspects of the main window
root.title("Alignment Selector")
root.geometry('500x300')

#Label and text entry for the name of the to-be-created training set
Label(root, text="Enter the sequence you wish to search", font=('Calibri 10')).place(x=150,y=100)
searchEntry = Entry(root, width= 40)
searchEntry.place(x=75, y=125)

#allows user to see the alignment in a fasta file
def ResultViewer():
    #variables must be declared global to properly function with Tkinter
    global button
    searchE = searchEntry.get()

    #Creates the secondary window where the alignment is displayed
    rv = Toplevel(root)
    rv.title("Viewing Sequence Results")
    rv.geometry('800x600')
    rv.configure(bg='green')

    tree = ttk.Treeview(rv, column=("SeqID","SeqName","Seq","ResID","SID"), show='headings')
    tree.column("SeqID", anchor=tkinter.CENTER)
    tree.heading("SeqID", text="SequenceID")
    tree.pack()

    #conduct query
    searchQuery = ("""SELECT SequenceID FROM Sequence WHERE SequenceName = ?""")
    c.execute(searchQuery, (searchE,))
    searchResults = c.fetchall()

    for row in searchResults:
        print(row)
        tree.insert(row, tkinter.END, values=row)

    button = Button(rv, text="Exit",command=rv.destroy)
    button.pack()

    rv.mainloop()

#closes the program - destroys everything
def close():
    root.destroy()

#submission button
searchButton = Button(root, text="SEarch up sequnce", command=ResultViewer, pady=10)
searchButton.place(x=150, y=225)

#Button to quite the program
ExitButton = Button(root, text="Exit", command=close, pady=10)
ExitButton.place(x=0,y=0)

#runs the program
root.mainloop()

"""
tree.column("SeqName", anchor=tkinter.CENTER)
    tree.heading("SeqName", text="Name")
    tree.column("Seq", anchor=tkinter.CENTER)
    tree.heading("Seq", text="Sequence")
    tree.column("ResID", anchor=tkinter.CENTER)
    tree.heading("ResID", text="ResearcherID")
    tree.column("SID", anchor=tkinter.CENTER)
    tree.heading("SID", text="SampleID")
"""