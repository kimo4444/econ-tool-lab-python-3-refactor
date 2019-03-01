import tkinter as tk
from PIL import ImageTk, Image
import sqlite3
import menu
import os
import bivariate
import quandl
import pandas
import descriptiveStats


class Application (tk.Frame):
    def __init__(self, master='None'):
        super().__init__(master)
        self.connectDb(os.path.dirname(
            os.path.realpath(__file__))+'/EconLabTool.db')
        self.create_widgets()
        self.grid()

    def connectDb(self, path):
        self.dbConnection = sqlite3.connect(path)
        # df = pandas.read_csv(
        #     'CSV/Civilian Labor Force Participation Rate (1948-2019).csv')
        # df.to_sql('Civilian Labor Force Participation Rate (1948-2019)',
        #           self.dbConnection)

    def create_widgets(self):
        cursor = self.dbConnection.cursor()

        self.img = ImageTk.PhotoImage(
            Image.open("logo.png"))
        self.appLogo = tk.Label(self, image=self.img)
        self.appLogo.grid(row=0, column=1, columnspan=3, sticky='NW')

        descriptiveStats.plot_and_analyze(self, cursor)

        self.quit = tk.Button(self, text="Exit",
                              command=self.master.destroy)
        self.quit.grid(row=0, column=17, ipadx=20, ipady=5)
        self.corrButton = tk.Button(
            self, text="Bivariate Analysis", command=self.createCorrelationFrame, font=('Helvetica', 16))
        self.corrButton.grid(row=1, pady=20, sticky='NW')

    def createCorrelationFrame(self):
        corrFrame = tk.Toplevel(root)
        corrFrame.geometry('800x900')
        cursor = self.dbConnection.cursor()
        bivariate.correlation(corrFrame, cursor)


root = tk.Tk()
root.title('EconToolLab')
root.geometry("900x900")
app = Application(master=root)
app.mainloop()
