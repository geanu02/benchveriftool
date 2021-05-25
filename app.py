# Import the tkinter module
import tkinter
#from tkPDFViewer import tkPDFViewer as pdf
import chrisproject
from tkdocviewer import *


def clear_screen():
    question_menu.pack_forget()
    # v2.pack_forget()
    v1.pack_forget()
    download_button.pack_forget()
    reset_button.pack_forget()


def main_page():
    options_list = chrisproject.client_list()
    global value_inside
    value_inside = tkinter.StringVar(root)
    value_inside.set("Select an Option")
    global question_menu
    question_menu = tkinter.OptionMenu(root, value_inside, *options_list)
    question_menu.pack()
    global submit_button
    submit_button = tkinter.Button(root,
                                   text='Generate Report',
                                   command=lambda: full_function())
    submit_button.pack()

    global v1
    # v1 = pdf.ShowPdf()
    v1 = DocViewer(root)
    v1.pack(side="top", expand=1, fill="both")
    #global v2
    # v2 = pdf.ShowPdf()


def clear_and_main():
    clear_screen()
    main_page()


def full_function():
    submit_button.pack_forget()
    global download_button
    global reset_button
    client_name = value_inside.get()
    client_index = chrisproject.return_c_num(client_name)
    filename = chrisproject.produce_pdf(client_index)
    print("Filename for {0} exists: {1}".format(client_name, filename))
    # v2 = v1.pdf_view(root, pdf_location=filename, width=80, height=70)
    # v2.pack()
    v1.display_file(filename)
    download_button = tkinter.Button(root, text='Download PDF', command=None)
    download_button.pack()
    reset_button = tkinter.Button(root,
                                  text='Start Over',
                                  command=lambda: clear_and_main())
    reset_button.pack()


root = tkinter.Tk()
root.title("BlueMark Verification Report")
root.geometry("820x1225")

main_page()

root.mainloop()
