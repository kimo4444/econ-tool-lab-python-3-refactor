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


def create_checkbox(frame, variable, text, row, column):
    return tk.Checkbutton(frame,  onvalue=1, variable=variable, offvalue=0, text=text).grid(
        row=row, column=column, sticky='W', pady=(15, 0))


def createLabel(frame, text, font, row, column):
    return tk.Label(frame, text=text,
                    font=font).grid(row=row, column=column, pady=(26, 0), sticky='W')


def plot_and_analyze(self, cursor):

    stat_frame = tk.Frame(self)
    stat_frame.grid_columnconfigure(0, minsize=200)  # <<<
    stat_frame.grid_columnconfigure(4, minsize=300)

    chosenIndicator = tk.StringVar()

    checkedMax = tk.IntVar()
    checkedMin = tk.IntVar()
    checkedMean = tk.IntVar()
    checkedStd = tk.IntVar()
    checkedVar = tk.IntVar()
    checkedRange = tk.IntVar()
    checkedMedian = tk.IntVar()
    checkedPlot = tk.IntVar()
    checkedHist = tk.IntVar()
    values = []
    dates = []
    color = tk.StringVar()
    plotTitle = tk.StringVar()
    menu.create_nestedmenu(stat_frame, 1, chosenIndicator)

    def query_Db():
        cursor.execute(
            'SELECT min(strftime("%Y", date)), max(strftime("%Y", date)) from [' + chosenIndicator.get()+']')
        for column in cursor:
            minYear = int(column[0])
            maxYear = int(column[1])

        if startYear.get() != '':
            if (int(startYear.get()) < minYear or int(startYear.get()) > maxYear) or (int(endYear.get()) < minYear or int(endYear.get()) > maxYear):
                tk.messagebox.showerror(
                    "Error", "Input years are out of range. The correct range is " + str(minYear) + ' - ' + str(maxYear))

            else:
                cursor.execute('SELECT * from [' + chosenIndicator.get()+'] where strftime("%Y", date) between "' +
                               startYear.get() + '" and "' + endYear.get() + '" order by date asc')
                plot()
        if startYear.get() == '':
            cursor.execute(
                'SELECT * from [' + chosenIndicator.get()+'] order by date asc')
            plot()

    def plot():
        print('hello')

        del dates[:]
        del values[:]
        for column in cursor:
            dates.append(str(column[0]))
            values.append(column[1])
            binNumber = len(values)
            index = 0
        y = values

        statbox = tk.Listbox(stat_frame, font=(
            'Helvetica', 17), borderwidth=0, width=25)
        if checkedMax.get():
            maxim = np.max(values)
            statbox.insert(tk.END, 'Maximum  ' + str(maxim))

        if checkedMin.get() == 1:
            minim = np.min(values)
            statbox.insert(tk.END, 'Minimum  ' + str(minim))

        if checkedMean.get() == 1:
            mean = np.average(values)
            statbox.insert(tk.END, 'Mean  ' + str(mean))

        if checkedStd.get() == 1:
            stdDev = np.std(values)
            statbox.insert(tk.END, 'Standard deviation ' + str(stdDev))

        if checkedMedian.get() == 1:
            median = np.median(values)
            statbox.insert(tk.END, 'Median value is ' + str(median))

        if checkedRange.get() == 1:
            rang = np.max(values) - np.min(values)
            statbox.insert(tk.END, 'Range ' + str(rang))

        statbox.grid(row=1, column=3)

        if checkedPlot.get() == 1:

            fig, axes = plt.subplots()
            axes.xaxis_date()
            fig.autofmt_xdate()

            axes.set_xlabel(xAxis.get() or 'Year')
            axes.set_ylabel(yAxis.get() or 'Value')
            x = mdates.datestr2num(dates)
            axes.set_title(plotTitle.get() or chosenIndicator.get())
            axes.plot(x, y, color=color.get())
            plt.show()
            plt.clf()
            plt.cla()
            plt.close()

        if checkedHist.get() == 1:
            fig, axes = plt.subplots()
            axes.set_title(plotTitle.get() or chosenIndicator.get())
            axes.set_xlabel(xAxis.get() or 'Value')
            axes.set_ylabel(yAxis.get() or 'Percent')
            # calculating default optimal number of bins(rounded to the nearest whole number) using
            # Sturges Rule in case not provided by the user

            k = int(round(1 + (3.322*np.log10(binNumber))))
            x = int(binEntry.get() or k)

            axes.hist(y, bins=x, rwidth=0.3, normed=True, color=color.get())
            plt.show()
            plt.clf()
            plt.cla()
            plt.close()


# creating statistics checkbox section
    descStatLabel = tk.Label(
        stat_frame, text='Descriptive Statistics:', font=('Helvetica 18 underline'))
    descStatLabel.grid(row=0, column=0)
    variance = create_checkbox(stat_frame, checkedVar, 'Variance', 1, 0)
    stdDev = create_checkbox(stat_frame, checkedStd, 'Deviation', 1, 1)
    mean = create_checkbox(stat_frame, checkedMean, 'Mean', 2, 0)
    stat_frame.grid(row=2, column=0, padx=(30, 0))
    median = create_checkbox(stat_frame, checkedMedian, 'Median', 2, 1)
    minValue = create_checkbox(stat_frame, checkedMin, 'Minimum', 3, 0)
    maxValue = create_checkbox(stat_frame, checkedMax, 'Maximum', 3, 1)
    rangeValue = create_checkbox(stat_frame, checkedRange, 'Range', 4, 0)

    createLabel(stat_frame, 'Plot Type:',
                ('Helvetica 18 underline'), 5, 0)

    plotValue = create_checkbox(
        stat_frame, checkedPlot, 'Time Series Graph', 7, 0)

    histValue = create_checkbox(stat_frame, checkedHist, 'Histogram', 7, 1)

    createLabel(stat_frame, 'Start Year',
                ('Helvetica 14'), 8, 0)
    startYear = tk.Entry(stat_frame)
    startYear.grid(row=8, column=1, sticky='SW')

    createLabel(stat_frame, 'End Year',
                ('Helvetica 14'), 9, 0)

    endYear = tk.Entry(stat_frame)
    endYear.grid(row=9, column=1, sticky='SW')

    # checkbuttons for custom styling the plot

    createLabel(stat_frame, 'Custom Styles:',
                ('Helvetica 15 underline '), 11, 0)

    color.set('#00468b')
    colorPick = tk.OptionMenu(stat_frame, color, 'red', 'green', 'black', 'blue',
                              'orange', 'grey').grid(row=12, pady=(15, 0), sticky='W')

    createLabel(stat_frame, 'Plot Title', ('Helvetica 14'), 14, 0)

    plotTitle = tk.Entry(stat_frame)
    plotTitle.grid(row=14, column=1, sticky='SW')

    createLabel(stat_frame, 'Y-axis', ('Helvetica 14'), 15, 0)

    yAxis = tk.Entry(stat_frame)
    yAxis.grid(row=15, column=1)
    createLabel(stat_frame, 'X-axis', ('Helvetica 14'), 16, 0)
    xAxis = tk.Entry(stat_frame)
    xAxis.grid(row=16, column=1)

    # choosing the bin number for the histogram
    createLabel(stat_frame, 'Number of bins',
                ('Helvetica 14'), 17, 0)
    binEntry = tk.Entry(stat_frame)
    binEntry.grid(row=17, column=1)

    submitButton = tk.Button(stat_frame, text='Submit',
                             width=10, command=query_Db)
    submitButton.grid(row=18, column=1,  padx=(
        75, 0), pady=(20, 0), sticky='W')
