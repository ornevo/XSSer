from Tkinter import *
from ttk import Style, Button, Frame
import thread

from XSSer import XSSer

TITLE = "XS10"
SUBTITLE = "(aka XSSer)"
LABELS = {
    "domain_lbl":       "Domain to scan:",
    "options_title_lbl": "Options:",
    "quick_scan_lbl":   "Quick scan",
    "shallow_scan_lbl": "Shallow scan",
    "submit_btn":       "Scan"
}
FONT = "Helvetica"
INPUTS_NAME = "crafted_inp.txt"

UNMATCHING_DOMAIN_ERR = "Oops: It seems like the domain you specified is not" \
                        " in the expected format:\nhttp://yourdomain.com"
NO_ERRORS_STR = "No errors."


class GUI(Frame):

    def __init__(self, root):
        Frame.__init__(self, root)
        self.parent = root
        self.quick_scan = BooleanVar()
        self.domain = StringVar()
        self.errors = StringVar(value=NO_ERRORS_STR)

        self._next_row = 6

        self.inps = self.get_inputs_list()

        self.init_ui()

    def init_ui(self):
        self.parent.title(TITLE)
        self.pack(fill=BOTH, expand=1)
        self.style = Style()
        self.style.theme_use("default")

        # Titles
        title = Label(self, text=TITLE, font=(FONT, 36))
        title.grid(row=0, columnspan=3, pady=(20, 0), padx=20)

        subtitle = Label(self, text=SUBTITLE, font=(FONT, 10))
        subtitle.grid(row=1, columnspan=3, pady=(0, 13))

        # Form
        # Domain
        domain_label = Label(self, text=LABELS["domain_lbl"], font=(FONT, 11))
        domain_label.grid(row=2, sticky=E, padx=(20, 10))
        domain_input = Entry(self, width=75, textvariable=self.domain)
        domain_input.grid(row=2, column=1, padx=(0, 20), sticky=W)

        # Options
        options_label = Label(self, text=LABELS["options_title_lbl"],
                              font=(FONT, 11))
        options_label.grid(row=3, sticky=E)

        quick_scan_checkbox = Checkbutton(self, text=LABELS["quick_scan_lbl"],
                                          font=(FONT, 9),
                                          variable=self.quick_scan)
        quick_scan_checkbox.grid(row=3, column=1, sticky=W)

        # Submit
        submit_btn = Button(self, text=LABELS["submit_btn"],
                            command=self.on_click)
        submit_btn.grid(row=4, columnspan=3, pady=10)

        # Errors
        errors_lbl = Label(self, textvariable=self.errors, font=(FONT, 11),
                           fg="red")
        errors_lbl.grid(row=5, columnspan=2, padx=20, pady=(10, 25), sticky=W)

    def on_click(self):
        if not self.valid_domain():
            self.errors.set(UNMATCHING_DOMAIN_ERR)
            return
        else:
            self.errors.set(NO_ERRORS_STR)
            self.init_scan()

    def valid_domain(self):
        """
        :return: True/False, indicating whether the submitted domain is valid
        """
        url = self.domain.get()
        return (url.startswith("http://") or url.startswith("https://")) and \
            url.find(".") != -1 and url[-1] != '.' and url.find(" ") == -1

    def init_scan(self):
        title = Label(self, text=self.domain.get(), font=(FONT, 11))
        title.grid(row=self._next_row, sticky=N)

        scrollbar = Scrollbar(self)
        scrollbar.grid(row=self._next_row+1, column=2, sticky=NSEW)

        status_box = Listbox(self, yscrollcommand=scrollbar.set)
        status_box.grid(row=self._next_row+1, column=1, padx=(0, 20),
                        sticky=NSEW)

        scanner = XSSer(self.domain.get(), self.inps, self.quick_scan.get(),
                        status_box)

        collapse_btn = Button(self, text="Toggle Log",
                              command=scanner.toggle_log)
        collapse_btn.grid(row=self._next_row, column=1)

        self._next_row += 2

        thread.start_new_thread(scanner.scan, ())

    def get_inputs_list(self):
        """
        Reads the inputs from their file and returns them as a list
        :return: The inputs list
        """
        ret = ""
        with open(INPUTS_NAME, "rt") as inps_f:
            ret = inps_f.read().split("\n")
        return ret[:-1]  # To remove the space in the end


def center(root):
    root.update_idletasks()
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    root.geometry("%dx%d+%d+%d" % (size + (x, y)))


root = Tk()
# root.resizable(0,0)  # Disable resizing
ex = GUI(root)
center(root)

root.mainloop()
