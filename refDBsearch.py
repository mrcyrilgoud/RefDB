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
Label(root, text="Enter the protein you wish to search", font=('Calibri 10')).place(x=150,y=50)
searchEntry = Entry(root, width= 40)
searchEntry.place(x=75, y=75)

#Label and text entry for the name of the to-be-created training set
Label(root, text="Enter the sequence you wish to search", font=('Calibri 10')).place(x=150,y=125)
seqEntry = Entry(root, width= 40)
seqEntry.place(x=75, y=150)

def seqSearch():
    qw = tkinter.Tk()

    # Specifies basic aspects of the query window
    qw.title("Query Result")
    qw.configure(background='black')
    width = 400
    height = 300
    qw.geometry(f'{width}x{height}')

    # closes the query
    def Close():
        qw.destroy()

    # button to close the query window
    CloseButton = Button(qw, text="Close", command=Close, padx=20, pady=10)
    CloseButton.place(x=10, y=10)

    try:
        # execute any query from the queryBox
        c.execute('SELECT * FROM Sequence WHERE Sequence= ?', (seqEntry.get(),))
        des = [tuple[0] for tuple in c.description]
        outputs = c.fetchall()

        # create table to display query
        table_frame = Frame(qw)
        table_frame.pack()
        table_frame.place(x=10, y=60)
        query_table = ttk.Treeview(table_frame)
        query_table.pack()

        # output any query into output box
        query_table['columns'] = des
        query_table.column("#0", width=0, stretch=NO)
        width = 20
        height = 150

        # add columns to table and define width
        # for every new column make window bigger
        for head in des:
            query_table.column(head, anchor=CENTER, width=100)
            width += 100

        # resize the window
        qw.geometry(f'{width}x{height}')

        # insert the column names into the table
        query_table.heading("#0", text="", anchor=CENTER)
        for head in des:
            query_table.heading(head, text=head, anchor=CENTER)

        # insert query into the table
        # for every item inserted, make window taller
        for x in range(len(outputs)):
            query_table.insert(parent='', index='end', iid=x, text='', values=outputs[x])
            height += 50

        # resize the window
        qw.geometry(f'{width}x{height}')
    except:
        Label(qw, text="Something wrong have occur", font=('Calibri 15'), bg='black').place(x=10, y=60)

    qw.mainloop()

def proteinSearch():
    qw = tkinter.Tk()

    # Specifies basic aspects of the query window
    qw.title("Query Result")
    qw.configure(background='black')
    width = 400
    height = 300
    qw.geometry(f'{width}x{height}')

    # closes the query
    def Close():
        qw.destroy()

    # button to close the query window
    CloseButton = Button(qw, text="Close", command=Close, padx=20, pady=10)
    CloseButton.place(x=10, y=10)

    try:
        # execute any query from the queryBox
        c.execute('SELECT * FROM Sequence WHERE SequenceName= ?', (searchEntry.get(),))
        des = [tuple[0] for tuple in c.description]
        outputs = c.fetchall()

        # create table to display query
        table_frame = Frame(qw)
        table_frame.pack()
        table_frame.place(x=10, y=60)
        query_table = ttk.Treeview(table_frame)
        query_table.pack()

        # output any query into output box
        query_table['columns'] = des
        query_table.column("#0", width=0, stretch=NO)
        width = 20
        height = 150

        # add columns to table and define width
        # for every new column make window bigger
        for head in des:
            query_table.column(head, anchor=CENTER, width=100)
            width += 100

        # resize the window
        qw.geometry(f'{width}x{height}')

        # insert the column names into the table
        query_table.heading("#0", text="", anchor=CENTER)
        for head in des:
            query_table.heading(head, text=head, anchor=CENTER)

        # insert query into the table
        # for every item inserted, make window taller
        for x in range(len(outputs)):
            query_table.insert(parent='', index='end', iid=x, text='', values=outputs[x])
            height += 50

        # resize the window
        qw.geometry(f'{width}x{height}')
    except:
        Label(qw, text="Something wrong have occur", font=('Calibri 15'), bg='black').place(x=10, y=60)

    qw.mainloop()

#closes the program - destroys everything
def close():
    root.destroy()

#submission button
searchButton = Button(root, text="Search up protein", command=proteinSearch, pady=10)
searchButton.place(x=150, y=200)

#submission button
searchButton = Button(root, text="Search up sequence", command=seqSearch, pady=10)
searchButton.place(x=150, y=250)

#Button to quite the program
ExitButton = Button(root, text="Exit", command=close, pady=10)
ExitButton.place(x=0,y=0)

#runs the program
root.mainloop()
