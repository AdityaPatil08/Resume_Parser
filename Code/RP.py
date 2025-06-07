from tkinter import *
from tkinter import ttk
import tkinter.messagebox as mb
from tkinter import ttk
import sqlite3
from tkinter import filedialog as fd    
import os                                
import shutil
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
import docx2txt
import nltk
import pandas as pd
import re
from pdfminer.high_level import extract_text
import tkinter.messagebox
from tkinter import font
import spacy

nlp = spacy.load('en_core_web_sm') 
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('maxent_ne_chunker_tab')

headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)

def login():
    if name_strvar.get()=="siesgst" and contact_strvar.get()=="1234":
        open_win()

    else:
        t = tkinter.messagebox.showinfo("INVALID USERNAME OR PASSWORD ", "YOU HAVE ENTERED INVALID USERNAME OR PASSWORD  ")
        loginid.delete(0,END)
        password.delete(0,END)

def extract_text_from_docx(docx_path):
    txt = docx2txt.process(docx_path)
    if txt:
        return txt.replace('\t', ' ')
    return None

def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

def extract_names(txt):
    person_names = []
 
    for sent in nltk.sent_tokenize(txt):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                person_names.append(
                    ' '.join(chunk_leave[0] for chunk_leave in chunk.leaves())
                )
    print("Name:")
    return person_names

data = pd.read_csv("skills.csv")     
skills = list(data.columns.values)
skillset = []

def extract_skills(input_text):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(input_text)
 
    filtered_tokens = [w for w in word_tokens if w not in stop_words]
 
    filtered_tokens = [w for w in word_tokens if w.isalpha()]
 
    bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))
 
    found_skills = set()
 
    for token in filtered_tokens:
        if token.lower() in skills:
            found_skills.add(token)
 
    for ngram in bigrams_trigrams:
        if ngram.lower() in skills:
            found_skills.add(ngram)
 
    return found_skills

RESERVED_WORDS = [
    'school', 'college', 'university', 'academy', 'faculty', 'institute', 'Institute', 'B.E.', 'B.E', 'B.S', 'M.E', 'M.E.', 
    'M.S', 'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 'SSC', 'HSC', 'CBSE', 'ICSE', '10th', '12th', 
    'Bachelor of Science', 'Master of Science', 'Bachelor', 'Master', 'PhD', 'Doctor', 
    'Engineering', 'Technology', 'Arts', 'Commerce'
]

def extract_education(input_text):
    doc = nlp(input_text)
    education = set()
    lines = input_text.splitlines()
    
    # Check each line for reserved words
    for line in lines:
        for word in RESERVED_WORDS:
            if word.lower() in line.lower():
                education.add(word)
                
    for ent in doc.ents:
        # Check for organizations (which may indicate educational institutions)
        if ent.label_ == "ORG":
            for word in RESERVED_WORDS:
                if word.lower() in ent.text.lower():
                    education.add(ent.text)
    
    return education

EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')

def extract_emails(resume_text):
    return re.findall(EMAIL_REG, resume_text)

PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')

def extract_phone(resume_text):
    return re.findall(PHONE_REG, resume_text)

JOB_TITLES = [
    'engineer', 'developer', 'manager', 'analyst', 'consultant', 'intern', 'officer',
    'executive', 'administrator', 'designer', 'architect', 'scientist', 'researcher'
]


DATE_PATTERN = r'(?<!\d)[01]\d[-/]\d{4}(?!\d)'

def extract_experience_dates(input_text):
    experience_dates = []

    # Find all matching date patterns in the input text
    dates = re.findall(DATE_PATTERN, input_text)

    if len(dates) > 0:
        print('experience: from', dates[0], 'to', dates[1] if len(dates) > 1 else 'present')

def open_file():
   filetypes = (
        ('doc files', '*.docx'),
        ('All files', '*.*')
    )
   file = filedialog.askopenfile(mode='r', filetypes=filetypes)
   if file:
       text = extract_text_from_docx(file.name)
    #    print(text)
       names = extract_names(text)
       if names:
           print(names[0])
           
       text = extract_text_from_docx(file.name)
       skillset = extract_skills(text)
       for skills in skillset:
           print("skills:",skills)
       
       
       text = extract_text_from_docx(file.name)
       education_information = extract_education(text)
       print(education_information)
       
       text = extract_text_from_docx(file.name)
       emails = extract_emails(text)
       if emails:
           print("email:",emails[0])
           
       text = extract_text_from_docx(file.name)
       phone = extract_phone(text)
       if phone:
           print("Phone no:",phone[0])
           
       text = extract_text_from_docx(file.name)
       experience = extract_experience_dates(text)

def open_file_pdf():
    file2 = filedialog.askopenfile(mode='r', filetypes=[('PDF Files', '*.pdf')])
    if file2:
       text = extract_text_from_pdf(file2.name)
    #    print(text)
       names = extract_names(text)
       if names:
           print(names[0])
           
       text = extract_text_from_pdf(file2.name)
       skillset = extract_skills(text)
       for skills in skillset:
           print("skills:",skills)
       
       text = extract_text_from_pdf(file2.name)
       education_information = extract_education(text)
       print("Education:",education_information)
       
       text = extract_text_from_pdf(file2.name)
       emails = extract_emails(text)
       if emails:
           print("email:",emails[0])
           
       text = extract_text_from_pdf(file2.name)
       phone = extract_phone(text)
       if phone:
           print("Phone no:",phone[0])

       text = extract_text_from_pdf(file2.name)
       experience = extract_experience_dates(text)
       
        
        
    
def close_main():
   main.destroy()

main = Tk()
main.title('Resume Parser Login')
main.geometry('1000x600')
main.resizable(0, 0)

# Setting the background color
main.config(bg='#F4F4F9')

# Frame for the login section
f = Frame(main, height=580, width=980, bg='#344955', bd=5)
f.place(x=10, y=10)

# Fonts
headlabelfont = ('Helvetica', 30, 'bold')
labelfont = ('Helvetica', 15)
entryfont = ('Helvetica', 12)

def open_win():
    new = Toplevel(main)
    new.geometry("750x500")
    new.title("Main Menu")
    new.config(bg='#F4A261')

    Label(new, text="Please select the Resume", font=('Helvetica 17 bold'), bg='#F4A261', fg='white').pack(pady=30)
    Button(new, text='Browse Docx', bg='#264653', fg='white', font=labelfont, command=open_file, width=18).pack(pady=20)
    Button(new, text='Browse PDF', bg='#2A9D8F', fg='white', font=labelfont, command=open_file_pdf, width=18).pack(pady=20)

# Variables for user data
name_strvar = StringVar()
contact_strvar = StringVar()

# Title
Label(main, text="RESUME PARSER", font=headlabelfont, bg='#F4F4F9', fg='#E76F51').pack(side=TOP, fill=X, pady=20)

# Labels and Entry boxes for User ID and Password
Label(main, text="User ID", font=labelfont, bg='#344955', fg='white').place(relx=0.300, rely=0.25)
Label(main, text="Password", font=labelfont, bg='#344955', fg='white').place(relx=0.285, rely=0.35)

loginid = Entry(main, width=35, textvariable=name_strvar, font=entryfont, bg='#E6E6FA', bd=3).place(x=400, rely=0.25)
password = Entry(main, show="*", width=35, textvariable=contact_strvar, font=entryfont, bg='#E6E6FA', bd=3).place(x=400, rely=0.35)

# Buttons for Confirm and Quit
Button(main, text='Confirm', bg='#2A9D8F', fg='white', font=labelfont, command=login, width=18).place(relx=0.400, rely=0.50)
Button(main, text="Quit", bg='#E76F51', fg='white', font=labelfont, command=close_main, width=18).place(relx=0.400, rely=0.60)

def openFolder():  
   the_folder = fd.askdirectory(title = "Select Folder to open")   
   os.startfile(the_folder)

tkinter.mainloop()
