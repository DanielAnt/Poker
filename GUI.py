from tkinter import *
from tkinter import messagebox


class Main:

    def __init__(self, master):
        self.master = master
        self.bgColor = 'white'
        self.main_frame = Frame(self.master, bg=self.bgColor, width=300, height=300 )
        self.main_frame.pack(fill=BOTH, expand=True)
        self.display_connection()

    def display_connection(self):
        if self.main_frame:
            for widget in self.main_frame.winfo_children():
                widget.destroy()
        grid_frame = Frame(self.main_frame, bg=self.bgColor)
        entry_frame = Frame(grid_frame, bg=self.bgColor)
        button_frame = Frame(grid_frame, bg=self.bgColor)
        IP_entry = Entry(entry_frame, justify="left")
        IP_label = Label(entry_frame, text="IP:", bg=self.bgColor)
        PORT_entry = Entry(entry_frame, justify="left")
        PORT_label = Label(entry_frame, text="PORT:", bg=self.bgColor)
        connect_button = Button(button_frame, text="Connect", width=10, command=self.connect, padx=15, pady=5)
        quit_button = Button(button_frame, text="Quit", width=10, command=self.quit, padx=15, pady=5)

        grid_frame.place(in_=self.main_frame, anchor="c", relx=.5, rely=.5)
        entry_frame.pack(side=TOP)
        button_frame.pack(side=TOP)
        IP_entry.grid(row=0, column=1, columnspan=1, padx=5, pady=5)
        IP_label.grid(row=0, column=0, sticky=E)
        PORT_entry.grid(row=1, column=1, columnspan=1, padx=5, pady=5)
        PORT_label.grid(row=1, column=0, sticky=E)
        connect_button.grid(row=2, column=0, padx=15, pady=5)
        quit_button.grid(row=2, column=1, padx=15, pady=5)

    def connect(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        creation_frame = Frame(self.main_frame, bg=self.bgColor)
        games_frame = Frame(self.main_frame, bg=self.bgColor)
        creation_frame.pack(side=LEFT)
        games_frame.pack(side=LEFT)

        name_label = Label(creation_frame, text="NAME", bg=self.bgColor)
        name_entry = Entry(creation_frame, justify="left")
        min_label = Label(creation_frame, text="MIN", bg=self.bgColor)
        min_entry = Entry(creation_frame, justify="left")
        max_label = Label(creation_frame, text="MAX", bg=self.bgColor)
        max_entry = Entry(creation_frame, justify="left")
        blind_label = Label(creation_frame, text="BLINDS", bg=self.bgColor)
        blind_entry = Entry(creation_frame, justify="left")
        create_button = Button(creation_frame, text="CREATE TABLE", command=self.create_table)
        n = 0
        name_label.grid(row=n, column=0, pady=10)
        name_entry.grid(row=n, column=1, pady=10)
        n += 1
        min_label.grid(row=n, column=0, pady=10)
        min_entry.grid(row=n, column=1, pady=10)
        n += 1
        max_label.grid(row=n, column=0, pady=10)
        max_entry.grid(row=n, column=1, pady=10)
        n += 1
        blind_label.grid(row=n, column=0, pady=10)
        blind_entry.grid(row=n, column=1, pady=10)
        n += 1
        create_button.grid(row=n, column=0, columnspan=2, pady=10, sticky=S)

        games_listbox = Listbox(games_frame,width=30, height=10,justify=LEFT)
        games_join_button = Button(games_frame, text="JOIN", width=11)
        games_refresh_button = Button(games_frame, text="REFRESH", width=11)

        games_listbox.grid(row=0, column=0,columnspan=2, pady=10, padx=5)
        games_join_button.grid(row=1, column=0, pady=10)
        games_refresh_button.grid(row=1, column=1,pady=10)

    def create_table(self):
        pass

    @staticmethod
    def quit():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            quit()


if __name__ == '__main__':

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            quit()

    root = Tk()
    Main(root)
    root.title('Poker')
    root.resizable(False,False)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
