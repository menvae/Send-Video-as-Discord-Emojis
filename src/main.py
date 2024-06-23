from server import run_background, run
from Client import InvalidToken
from customtkinter import *
from tkinter import messagebox
import screeninfo as sc
from multiprocessing import Process
import os
import logging

logging.basicConfig(filename='Program Error.log', level=logging.INFO)

SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0
WINDOW_WIDTH = 620
WINDOW_HEIGHT = 420

WINDOW_COLOR = "#232226"
FRAME_COLOR = "#2b2b2b"

Path: str

action: int = 0
interval: int = 0
mode: int = 0
loop: bool = False
start_sending = False

for monitor in sc.get_monitors():
    if monitor.is_primary is True:
        SCREEN_WIDTH = monitor.width
        SCREEN_HEIGHT = monitor.height


def getPath(Entry: CTkEntry) -> None:
    global Path
    Path = filedialog.askopenfilename(initialdir=os.getcwd(), filetypes=[("", ".vtd")])

    Entry.delete(0, END)
    Entry.insert(0, Path)


def option_select(value: str) -> None:
    global action

    if value == "Send only":
        action = 2
        MessageEntry.configure(state=DISABLED)
    elif value == "Edit only":
        action = 1
        MessageEntry.configure(state=NORMAL)
    else:
        action = 0
        MessageEntry.configure(state=DISABLED)


def checkbox_select() -> None:
    global mode
    value = int(SendEvery.get())
    mode = value


def loop_select() -> None:
    global loop
    value = int(LoopSwitch.get())
    if value == 1:
        loop = True
        return
    loop = False


def initialize() -> None:
    global start_sending
    start_sending = True


def check() -> None:
    global start_sending
    if start_sending is True:
        try:
            start()
        except Exception:
            logging.exception('An error occurred when starting')
            NoticeLabel.configure(
                text="An error has occurred when starting\nopen an issue on github with the Program Error log\nif this issue persists",
                text_color="#CE7476")

        start_sending = False
    root.after(200, check)


def start() -> None:
    global mode, interval, action, loop

    Path = PathEntry.get()

    if not os.path.exists(Path):
        messagebox.showerror("Error", "Path doesn't exist")
        return

    try:
        if MessageEntry.cget('state') == DISABLED:
            message_id = 0
        else:
            message_id = int(MessageEntry.get())
        channel_id = int(ChannelEntry.get())
    except ValueError:
        messagebox.showerror("Error", "Message ID and channel ID must be numbers")
        return

    if mode == 1:
        try:
            interval = int(interval)
        except ValueError:
            messagebox.showerror("Error", "Interval must be a number")
            return
    try:
        # run(channel_id, message_id, Path, action, loop, mode, interval)
        process = Process(target=run, args=(channel_id, message_id, Path, action, loop, mode, interval))
        Process.daemon = False
        process.start()
        NoticeLabel.configure(text="Process has started in the background\n you can close this window",
                              text_color="#83C5A5")
    except InvalidToken:
        logging.exception('An error occurred when starting')
        messagebox.showerror("Error", "Invalid Token has been entered in token.txt")
        return


root = CTk()

EntryFont = CTkFont(family='Arial', size=20)
ButtonFont = CTkFont(family='Arial', size=25)
XFont = CTkFont(family='Arial', size=15)

root.geometry(
    f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{(SCREEN_WIDTH // 2) - (WINDOW_WIDTH // 2)}+{(SCREEN_HEIGHT // 2) - (WINDOW_HEIGHT // 2)}'
)
root.resizable(FALSE, FALSE)
root.iconbitmap(f"{os.getcwd()}\\main_icon.ico")
root.title("Video to Emoji")
root.config(bg=WINDOW_COLOR)

MainFrame = CTkFrame(root, width=WINDOW_WIDTH - 50, height=WINDOW_HEIGHT - 50, corner_radius=10, fg_color=FRAME_COLOR)
OptionsMenu = CTkSegmentedButton(MainFrame, values=['Send only', 'Send then edit', 'Edit only'], font=EntryFont,
                                 selected_color="#65A686", selected_hover_color="#568D72", command=option_select)
OptionsMenu.set('Send only')
LoopSwitch = CTkSwitch(MainFrame, font=EntryFont, text="loop", fg_color=WINDOW_COLOR, progress_color="#65A686")

SendEvery = CTkCheckBox(MainFrame, text="Send every", font=EntryFont, hover_color="#65A686", fg_color="#65A686",
                        command=lambda: checkbox_select())
IntervalEntryBox = CTkEntry(MainFrame, width=46, height=30, font=EntryFont)
SecondsLabel = CTkLabel(MainFrame, font=EntryFont, text="Seconds")
ChannelEntry = CTkEntry(MainFrame, width=250, height=35, font=EntryFont, placeholder_text="Channel ID")
MessageEntry = CTkEntry(MainFrame, width=250, height=35, font=EntryFont, placeholder_text="Message ID", state=DISABLED)

PathEntry = CTkEntry(MainFrame, width=450, height=35, corner_radius=0, font=EntryFont,
                     placeholder_text=".vtd File Path")
PathBrowse = CTkButton(MainFrame, command=lambda: getPath(PathEntry),
                       text=BROWSE, width=50,
                       height=35, corner_radius=0,
                       fg_color="#FFFFFF", text_color="#000000", hover_color="#999999")

StartButton = CTkButton(MainFrame, font=ButtonFont, text="start", fg_color="#65A686", hover_color="#568D72", width=150,
                        height=40, command=lambda: initialize())
NoticeLabel = CTkLabel(MainFrame, font=XFont, text="Process has started in the background\n you can close this window",
                       text_color=FRAME_COLOR)

MainFrame.pack(expand=TRUE, fill=BOTH, padx=15, pady=15)
OptionsMenu.place(relx=0.22, rely=0.1)

LoopSwitch.place(relx=0.78, rely=0.24)

SendEvery.place(relx=0.25 + 0.02, rely=0.24)
IntervalEntryBox.place(relx=0.49 + 0.02, rely=0.24)
SecondsLabel.place(relx=0.58 + 0.02, rely=0.24)

ChannelEntry.place(relx=0.06, rely=0.35)
MessageEntry.place(relx=0.51, rely=0.35)

PathEntry.place(relx=0.07, rely=0.5)
PathBrowse.place(relx=0.82, rely=0.5)

StartButton.place(relx=0.38, rely=0.84)
NoticeLabel.place(relx=0.3, rely=0.68)
option_select('Send only')

if __name__ == '__main__':
    check()
    root.mainloop()
