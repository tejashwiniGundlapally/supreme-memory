import tkinter
from tkinter import *
import openpyxl
import numpy
import cv2
import pyzbar.pyzbar as pyzbar
import mysql.connector
import pyttsx3


def new(id):
    engine = pyttsx3.init()
    print("There is description for this barcode '{}' ".format(id.decode()))
    text = input(
        "Pleace enter description for this barcode '{}' : ".format(id.decode()))

    con = mysql.connector.connect(host="remotemysql.com", user="QGFMzjAjfn",
                                  password="4GH3QESgj4", database="QGFMzjAjfn")
    cursor = con.cursor()
    query = "INSERT INTO barcode (id_number,description) VALUES (%s, %s)"
    values = (id, text)
    cursor.execute(query, values)
    cursor.execute("commit")
    con.close()
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.say(text)
    engine.runAndWait()


def scan():
    engine = pyttsx3.init()
    i = 0
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while i < 1:
        _, frame = cap.read()
        decoded = pyzbar.decode(frame)
        for obj in decoded:
            print("This barcode is scan form Video Capture " +
                  str(obj.data.decode()))
            i = i+1
            id_number_code = obj.data
        cv2.imshow("QRCode", frame)
        if cv2.waitKey(5) == ord('q'):
            exit()

    mydb = mysql.connector.connect(
        host="remotemysql.com",
        user="QGFMzjAjfn",
        password="4GH3QESgj4",
        database="QGFMzjAjfn"
    )
    cv2.destroyAllWindows()
    mycursor = mydb.cursor()
    sql = "SELECT description FROM barcode WHERE id_number = %s"
    adr = (id_number_code, )
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchall()
    print(myresult)
    if len(myresult) == 0:
        return new(id_number_code)
    else:
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.say(myresult)
        engine.runAndWait()


top = tkinter.Tk()
top.geometry("300x250")
top.configure(bg='white')
top.title("BAR CODE SCANER")
top.resizable(False, False)
button = tkinter.Button(top, text="scan", font=(
    'Roboto', 10, 'bold'), bg="brown", fg="white", width="8", height="1", command=scan)
button.place(x=112, y=50)
top.mainloop()
