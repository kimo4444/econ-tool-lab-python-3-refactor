import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import menu
import tkinter as tk

import matplotlib
matplotlib.use("TkAgg")
plt.style.use('ggplot')


def createLabel(frame, text, font, row, column, verticalPadding, horizontalPadding):
    return tk.Label(frame, text=text,
                    font=font).grid(row=row, column=column, pady=verticalPadding, padx=horizontalPadding)


def correlation(frame, cursor):
    # dropdown menu fot selecting two variables for bivariate stats

    # menu.create_nestedmenu(frame, 2, chosenIndicator2)

    checkedScatter = tk.IntVar()
    checkedBivar = tk.IntVar()
    createLabel(frame, 'Bivariate Statistics',
                ('Helvetica 23 underline'), 0, 0, (40, 0), (40, 0))
    createLabel(frame, 'Start Year',
                ('Helvetica 17'), 3, 0, (40, 10), (60, 0))

    startYear = tk.Entry(frame)
    startYear.grid(row=3, column=1, pady=(40, 10))
    createLabel(frame, 'End Year',
                ('Helvetica 17'), 4, 0, (0, 0), (60, 0))

    endYear = tk.Entry(frame)
    endYear.grid(row=4, column=1)

    createLabel(frame, 'Plot Type:',
                ('Helvetica 23 underline'), 6, 0, (30, 0), (20, 0))

    tk.Checkbutton(frame,  variable=checkedScatter, text='Scatter Plot', font=(
        'Helvetica 15 underline')).grid(row=7, column=0,  padx=(40, 0), pady=(8, 10))
    tk.Checkbutton(frame,  variable=checkedBivar, text='Bivariate Plot', font=(
        'Helvetica 15 underline')).grid(row=7, column=1, pady=(8, 10))
    chosenIndicator = tk.StringVar()
    chosenIndicator2 = tk.StringVar()

    def scatter():
        values1 = []
        values2 = []
        dates1 = []
        dates2 = []
        x = []
        y = []

        del dates1[:]
        del values1[:]
        del dates2[:]
        del values2[:]

        cursor.execute(
            'SELECT min(strftime("%Y", date)), max(strftime("%Y", date)) from [' + chosenIndicator.get()+']')
        for column in cursor:
            minYear = int(column[0])
            maxYear = int(column[1])
        cursor.execute(
            'SELECT min(strftime("%Y", date)), max(strftime("%Y", date)) from [' + chosenIndicator2.get()+']')
        for column in cursor:
            minYear2 = int(column[0])
            maxYear2 = int(column[1])

        maxLower = max(minYear, minYear2)
        maxUpper = min(maxYear, maxYear2)

        if startYear.get() == '':
            tk.messagebox.showerror("Error", "Please input years")

        if startYear.get() != '':
            if ((int(startYear.get()) < minYear or int(startYear.get()) < minYear2) or (int(startYear.get()) > maxYear or int(startYear.get()) > maxYear2 or (int(endYear.get()) < minYear or int(endYear.get()) > maxYear))):
                tk.messagebox.showerror(
                    "Error", "Input years are out of range. The correct range is " + str(maxLower) + ' - ' + str(maxUpper))

            else:
                cursor.execute('SELECT * from [' + chosenIndicator.get()+'] where strftime("%Y", date) between "' +
                               startYear.get() + '" and "' + endYear.get() + '" order by date asc')
                for column in cursor:
                    values1.append(column[1])
                    dates1.append(column[0])
                    x = values1
                cursor.execute('SELECT * from [' + chosenIndicator2.get()+'] where strftime("%Y", date) between "' +
                               startYear.get() + '" and "' + endYear.get() + '" order by date asc')
                for column in cursor:
                    values2.append(column[1])
                    dates2.append(column[0])
                    y = values2

        covariance = np.cov(x, y)[0][1]
        correlation = np.corrcoef(x, y)[1][0]
        corrList = tk.Listbox(frame, font=(
            'Helvetica', 18), borderwidth=0, width=50)
        corrList.insert(
            tk.END, 'Correlation coefficient   ' + str(correlation))
        corrList.insert(
            tk.END, 'Covarience                    ' + str(covariance))
        corrList.grid(column=0, row=10, columnspan=2, padx=(60, 0), pady=30)

        if checkedScatter.get() == 1:
            fig, axes = plt.subplots()
            axes.set_title(chosenIndicator.get() +
                           ' and ' + chosenIndicator2.get())
            axes.set_xlabel(chosenIndicator.get())
            axes.set_ylabel(chosenIndicator2.get())
            axes.scatter(y, x, color='red')

        if checkedBivar.get() == 1:
            dates11 = mdates.datestr2num(dates1)
            dates22 = mdates.datestr2num(dates2)

            fig2, axes2 = plt.subplots()
            axes2.set_title(chosenIndicator.get() +
                            ' and ' + chosenIndicator2.get())
            axes2.set_xlabel(chosenIndicator.get() +
                             '\n' + chosenIndicator2.get())
            plot1, = axes2.plot(dates11, values1, color='red')
            plot2, = axes2.plot(dates22, values2, color='green')
            fig2.legend([plot1, plot2], [chosenIndicator.get(),
                                         chosenIndicator2.get()], 'upper right')
            axes2.xaxis_date()

        plt.show()
        plt.clf()
        plt.cla()
        plt.close()
    submitButton = tk.Button(frame, text='Plot', width=10, command=scatter)
    submitButton.grid(row=9, column=1,  padx=(60, 0), pady=(25, 0))
    menu.create_nestedmenu(frame, 1, chosenIndicator)
    menu.create_nestedmenu(frame, 2, chosenIndicator2)
