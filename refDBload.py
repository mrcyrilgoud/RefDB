#Importing Tkinter - Python GUI library

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox
import os

# Importing sqlite3
import sqlite3

# if 'ProteinSequence.db' already exist, delete it
if os.path.exists("ProteinSequence.db"):
    os.remove("ProteinSequence.db")

# Create the 'ProteinSequence.db' file
connect = sqlite3.connect('ProteinSequence.db')
if os.path.exists('ProteinSequence.db'):
    # create cursor to point in the database
    c = connect.cursor()

    # Create all tables
    # Create the Organism table
    c.execute("""
        CREATE TABLE Organism(
            SequenceOrganism TEXT NOT NULL PRIMARY KEY UNIQUE,
            GenusFamily TEXT NOT NULL,
            SequenceSource INTEGER NOT NULL
        )""")
    # Create the LAB table
    c.execute("""
        CREATE TABLE LAB(
            LabID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            LabAddress TEXT NOT NULL,
            LabName TEXT NOT NULL,
            LabZipCode INTEGER NOT NULL,
            LabState TEXT NOT NULL,
            LabCity TEXT NOT NULL
        )""")
    # Create the Institution table
    c.execute("""
        CREATE TABLE Institution(
            InstitutionID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            InstitutionName TEXT NOT NULL,
            InstitutionAddress TEXT NOT NULL,
            InstitutionCity TEXT NOT NULL,
            InstitutionZipCode INTEGER NOT NULL,
            InstitutionState TEXT NOT NULL
        )""")
    # Create the Mission table
    c.execute("""
        CREATE TABLE Mission(
            MissionID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            MissionSponsor TEXT NOT NULL,
            MissionName TEXT NOT NULL
        )""")
    # Create the Researcher table
    c.execute("""
        CREATE TABLE Researcher(
            ResearcherNumber INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            ResearcherFirstname TEXT NOT NULL,
            ResearcherLastName TEXT NOT NULL,
            ResearcherReputation INTEGER NOT NULL,
            InstitutionID INTEGER NOT NULL,
            FOREIGN KEY(InstitutionID) REFERENCES Institution(InstitutionID)
        )""")
    # Create the Sample table
    c.execute("""
        CREATE TABLE Sample(
            SampleID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            DateSampled DATE NOT NULL,
            TimeSampled TIME NOT NULL,
            SampleSource TEXT NOT NULL,
            SequenceOrganism TEXT NOT NULL,
            LabID INTEGER NOT NULL,
            MissionID INTEGER NOT NULL,
            FOREIGN KEY (SequenceOrganism) REFERENCES Organism(SequenceOrganism),
            FOREIGN KEY (LabID) REFERENCES Lab(LabID),
            FOREIGN KEY (MissionID) REFERENCES Mission(MissionID)
        )""")
    # Create the Sequence table
    c.execute("""
        CREATE TABLE Sequence(
            SequenceID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            SequenceName TEXT NOT NULL,
            Sequence TEXT NOT NULL,
            ResearcherNumber INTEGER NOT NULL,
            SampleID INTEGER NOT NULL,
            FOREIGN KEY (ResearcherNumber) REFERENCES Researcher(ResearcherNumber),
            FOREIGN KEY (SampleID) REFERENCES Sample(SampleID)
        )""")

    # commit the database
    connect.commit()

#the Tkinter root window
#First window that the user will see
root = tkinter.Tk()

#Specifies basic aspects of the main window
root.title("DB uploader")
root.geometry('500x300')

Label(root, text="Enter the researcher number", font=('Calibri 10')).place(x=150,y=50)
resIdEntry = Entry(root, width= 40)
resIdEntry.place(x=75, y=75)

Label(root, text="Enter the sample ID ", font=('Calibri 10')).place(x=150,y=125)
sidEntry = Entry(root, width= 40)
sidEntry.place(x=75, y=150)

#closes the program - destroys everything
def close():
    root.destroy()

#this function takes the input file and processes it
def submissionAl():
    #opens the file dialog and gets the filepath of the input file
    filePath = filedialog.askopenfilename()

    #Checks if the file is existent and in the correct format
    if not filePath:
        tkinter.messagebox.showerror("Canceled","operation canceled")
        return
    elif filePath.lower().endswith(('.fasta', '.fa', '.txt')):
        tkinter.messagebox.showinfo("File accepted","File to be submitted")
    else:
        tkinter.messagebox.showerror("File error", "Improper file type")
        return

    #reads the inputted file and stores all the strings in a list
    with open(filePath, 'r') as reader:
        linesFile = []
        seqLine = ""
        numSeqs = 0

        for lineRed in reader:
            if (lineRed.count(">") != 0):
                linesFile.append(seqLine)
                linesFile.append(lineRed)
                seqLine = ""
                numSeqs += 1
            else:
                seqLine += lineRed
    #takes care of certain edge case issues in the loop
    if(seqLine != ""):
        linesFile.append(seqLine)

    def_line=""
    sequence = ""
    resNum = resIdEntry.get()
    sampleID = sidEntry.get()
    insert_stmt = ("INSERT INTO Sequence(SequenceName, Sequence, ResearcherNumber, SampleID)"
                   "VALUES (?, ?, ?, ?)"
                   )

    #Creates the new output testing and training files
    for evLine in linesFile:
        if (evLine.count(">") != 0):
            record = (def_line, sequence, resNum, sampleID)
            c.execute(insert_stmt, record)

            def_line = evLine[1:-1]
            sequence = ""
        else:
            sequence = evLine
    connect.commit()

#submission button
submitButton = Button(root, text="Upload Sequences", command=submissionAl, pady=10)
submitButton.place(x=150, y=225)

#Button to quit the program
ExitButton = Button(root, text="Exit", command=close, pady=10)
ExitButton.place(x=0,y=0)

#runs the program
root.mainloop()