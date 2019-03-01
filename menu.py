import tkinter as tk
import menuData


def create_nestedmenu(frame, row, var):
    econIndicators = menuData.data
    # setting default indicator
    indicator = tk.StringVar()
    indicator.set('Gross Domestic Product (1947-2017)')
    # var = tk.StringVar()
    # var.set('Gross Domestic Product (1947-2017)')
    nestedMenu = tk.Menubutton(
        frame, textvariable=var, font=('Helvetica', 16))

    mainMenu = tk.Menu(nestedMenu, tearoff=False)
    nestedMenu.config(menu=mainMenu)

    for indicator in (econIndicators.keys()):
        option = tk.Menu(mainMenu)
        mainMenu.add_cascade(label=indicator, menu=option)
        mainMenu.add_separator()
        for nestedIndicator in econIndicators[indicator]:
            option.add_checkbutton(
                label=nestedIndicator, variable=var, onvalue=nestedIndicator, offvalue=0)
            option.add_separator()
    nestedMenu.grid(row=row, column=2, columnspan=8,
                    padx=20, pady=25, ipadx=20, ipady=5)
