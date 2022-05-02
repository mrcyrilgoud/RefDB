import os

# Importing Tkinter - Python GUI library
from tkinter import *
import tkinter.messagebox
from tkinter import ttk

# Importing sqlite3
import sqlite3

# Create the 'ProteinSequence.db' file
connect = sqlite3.connect('ProteinSequence.db')
c = connect.cursor()

# Tkinter main window
# First window that the user will see
main = tkinter.Tk()

# Specifies basic aspects of the main window
main.title("Protein Sequence Database Query")
main.configure(background='black')
main.geometry('800x300')

# Label and text entry for the query
Label(main, text="Query the Sequence Database", font=('Calibri 15'), bg='black').place(x=10, y=60)
queryBox = Entry(main, width=80)
queryBox.place(x=10, y=90)


# create the query window
def query():
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
        c.execute(queryBox.get())
        des = [tuple[0] for tuple in c.description]
        outputs = c.fetchall()

        # create table to display query
        # code referenced from https://pythonguides.com/python-tkinter-table-tutorial/
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


# button to start the database query
querybutton = Button(main, text="Submit", command=query, padx=20, pady=10)
querybutton.place(x=10, y=140)


# closes the main program - destroys everything (database and the window)
def Exit():
    connect.close()
    main.destroy()


# Button to quit the program
ExitButton = Button(main, text="Exit", command=Exit, padx=20, pady=10)
ExitButton.place(x=10, y=10)

# runs the program
main.mainloop()