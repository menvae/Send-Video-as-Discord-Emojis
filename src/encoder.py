import screeninfo as sc
from encode import encode, get_size, frames_progression, status, Gframes
from customtkinter import *
from tkinter import messagebox
from threading import Thread
from time import sleep
import os
import logging

logging.basicConfig(filename='Encoding Error.log', level=logging.INFO)


SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0
WINDOW_WIDTH = 620
WINDOW_HEIGHT = 420
WINDOW_COLOR = "#232226"
FRAME_COLOR = "#49474E"

VideoPath: str = ""
ExportPath: str

VIDEO_WIDTH: int = 0
VIDEO_HEIGHT: int = 0

for monitor in sc.get_monitors():
    if monitor.is_primary is True:
        SCREEN_WIDTH = monitor.width
        SCREEN_HEIGHT = monitor.height


def getVideoPath(Entry: CTkEntry, WidthEntry: CTkEntry, HeightEntry: CTkLabel) -> None:
    global VideoPath, VIDEO_WIDTH, VIDEO_HEIGHT
    VideoPath = filedialog.askopenfilename(initialdir=os.getcwd())
    VIDEO_WIDTH, VIDEO_HEIGHT = get_size(VideoPath)
    Entry.delete(0, END)
    Entry.insert(0, VideoPath)
    WidthEntry.delete(0, END)
    WidthEntry.insert(0, VIDEO_WIDTH)
    HeightEntry.configure(text=VIDEO_HEIGHT)


def getExportPath(Entry: CTkEntry) -> None:
    global ExportPath
    ExportPath = filedialog.askdirectory(initialdir=os.getcwd())
    Entry.delete(0, END)
    Entry.insert(0, ExportPath)


def calculate_height(Entry: CTkEntry, HeightLabel: CTkLabel, warning: CTkLabel) -> None:
    global VIDEO_WIDTH, VIDEO_HEIGHT, selected_width

    Width = Entry.get()

    try:
        int(Width)
    except:
        HeightLabel.configure(text='height')

    if Width in ('', None):
        HeightLabel.configure(text=VIDEO_HEIGHT)
        Entry.delete(0, END)
        Entry.insert(0, VIDEO_WIDTH)
        return
    elif Width in (0, '0'):
        HeightLabel.configure(text=0)
        return

    try:
        new_height = round((int(Width) / VIDEO_WIDTH) * VIDEO_HEIGHT)
    except ZeroDivisionError:
        new_height = 0

    HeightLabel.configure(text=new_height)

    if int(Width) * new_height > 2000:
        warning.configure(text_color="#c26163")
    else:
        warning.configure(text_color=FRAME_COLOR)


def ensure_height(Width) -> None:
    if not os.path.exists(VideoPath):
        messagebox.showwarning("Warning", "Video not choosen or doesn't exist")
        return

    if Width in (0, '0') or '.' in Width or not Width.isdigit():
        messagebox.showerror("error", "Width can only an integer number")
        return


def update_status(ProgressBar: CTkProgressBar, StatusText: CTkLabel) -> None:
    global status, frames_progression, Gframes

    started = False

    while True:
        from encode import status, frames_progression
        StatusText.configure(text=status)
        if status not in ("initializing", "not started") and started is False:
            from encode import Gframes
            started = True
            ProgressBar.configure(mode="determinate", progress_color="#6DCA6B")
            ProgressBar.stop()
            ProgressBar.stop()
            ProgressBar.set(0)
        if started is True:
            ProgressBar.set(max(0, min((frames_progression[0] / int(Gframes)), 1)))
        if status == "Done!":
            ProgressBar.stop()
            EncodeButton.configure(state=NORMAL)
            break
        # root.update_idletasks()
        sleep(0.1)


def start_encode(ProgressBar: CTkProgressBar, StatusText: CTkLabel) -> None:
    global VideoPath
    try:
        invert = False

        try:
            float(ContrastEntry.get())
            float(BrightnessEntry.get())
            int(FpsEntry.get())
        except ValueError:
            ContrastEntry.insert(0, 1)
            BrightnessEntry.insert(0, 0)
            messagebox.showerror("Error", "Contrast, brightness and fps must be a number")

        if not os.path.exists(VideoPath):
            messagebox.showerror("Error", "No video selected.")
            return
        if not os.path.exists(ExportPath):
            messagebox.showerror("Error", "No export path selected.")
            return
        if float(ContrastEntry.get()) < -2 or float(ContrastEntry.get()) > 2:
            messagebox.showerror("Error", "Contrast ranges from -2 to 2")
            return
        if float(ContrastEntry.get()) < -1 or float(ContrastEntry.get()) > 1:
            messagebox.showerror("Error", "Brightness ranges from -1 to 1")
            return
        if int(FpsEntry.get()) <= 0 or FpsEntry.get() in (None, ''):
            messagebox.showerror("Error", "fps cannot be zero or empty")
            return

        if int(InvertSwitch.get()) != 0:
            invert = True

        ProgressBar.configure(mode="indeterminate", progress_color="#6DCA6B")
        ProgressBar.set(0.3)
        ProgressBar.start()

        update_thread = Thread(target=update_status, args=(ProgressBar, StatusText), daemon=True)

        encode_thread = Thread(target=encode, args=(int(WidthEntry.get()), int(HeightLabel.cget('text')),
                                                    float(ContrastEntry.get()), float(BrightnessEntry.get()),
                                                    int(FpsEntry.get()), invert,
                                                    VideoPath, ExportPath, TitleEntry.get()), daemon=True)

        EncodeButton.configure(state=DISABLED)
        encode_thread.start()
        update_thread.start()
    except Exception:
        logging.exception('An error occurred when encoding')
        messagebox.showerror("An error occured", "An error has occurred when starting\nopen an issue on github with the Encoding Error log\nif this issue persists")

    # encode(int(WidthEntry.get()), int(HeightLabel.cget('text')),
    #        float(ContrastEntry.get()), float(BrightnessEntry.get()), float(FpsEntry.get()), invert,
    #        VideoPath, ExportPath, TitleEntry.get())


root = CTk()

PathLabelFont = CTkFont(family="Arial", size=20)
OptionsLabelFont = CTkFont(family="Arial", size=18)
EntryFont = CTkFont(family='Arial', size=17)
XFont = CTkFont(family='Arial', size=15)

selected_width = IntVar()
selected_height = IntVar()

root.iconbitmap(f"{os.getcwd()}\\encode_icon.ico")
root.title("Encoder")
root.geometry(
    f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{(SCREEN_WIDTH // 2) - (WINDOW_WIDTH // 2)}+{(SCREEN_HEIGHT // 2) - (WINDOW_HEIGHT // 2)}'
)

root.resizable(FALSE, FALSE)
root.config(bg=WINDOW_COLOR)

VideoPathGroup = CTkFrame(master=root, width=root.winfo_width() - 50, height=75, fg_color=FRAME_COLOR,
                          bg_color=WINDOW_COLOR,
                          corner_radius=20)
VideoPathLabel = CTkLabel(VideoPathGroup, text="Choose Video", anchor=CENTER, font=PathLabelFont)
VideoPathEntry = CTkEntry(VideoPathGroup, width=400, height=30, corner_radius=0, font=EntryFont)
VideoPathBrowse = CTkButton(VideoPathGroup, command=lambda: getVideoPath(VideoPathEntry, WidthEntry, HeightLabel),
                            text=BROWSE, width=50,
                            height=30, corner_radius=0,
                            fg_color="#FFFFFF", text_color="#000000", hover_color="#999999")

ExportPathGroup = CTkFrame(master=root, width=root.winfo_width() - 50, height=75, fg_color=FRAME_COLOR,
                           bg_color=WINDOW_COLOR,
                           corner_radius=20)
ExportPathLabel = CTkLabel(ExportPathGroup, text="Export to", anchor=CENTER, font=PathLabelFont)
ExportPathEntry = CTkEntry(ExportPathGroup, width=400, height=30, corner_radius=0, font=EntryFont)
ExportPathBrowse = CTkButton(ExportPathGroup, command=lambda: getExportPath(ExportPathEntry), text=BROWSE, width=50,
                             height=30, corner_radius=0,
                             fg_color="#FFFFFF", text_color="#000000", hover_color="#999999")

OptionsGroup = CTkFrame(master=root, width=root.winfo_width() - 50, height=70, fg_color=FRAME_COLOR,
                        bg_color=WINDOW_COLOR,
                        corner_radius=20)

OptionsTitleLabel = CTkLabel(OptionsGroup, text="Title", anchor=CENTER, font=OptionsLabelFont)
CharacterWarning = CTkLabel(OptionsGroup, text="Warning: size exceeds\nthe discord character limit", anchor=CENTER,
                            font=XFont, text_color=FRAME_COLOR)
TitleEntry = CTkEntry(OptionsGroup, width=220, height=30, corner_radius=0, font=PathLabelFont, placeholder_text="Title")
SizeFrame = CTkFrame(OptionsGroup, fg_color="#343638", border_color="#999999", border_width=1)
WidthEntry = CTkEntry(SizeFrame, width=58, height=25, corner_radius=0, font=EntryFont, placeholder_text="width",
                      fg_color="#343638", border_color="#343638", border_width=1)
XLabel = CTkLabel(SizeFrame, text="x", font=XFont)
HeightLabel = CTkLabel(SizeFrame, width=58, height=25, corner_radius=0, font=EntryFont, text="height")
ContrastEntry = CTkEntry(OptionsGroup, width=108, height=25, corner_radius=0, font=EntryFont,
                         placeholder_text="contrast: 1")
BrightnessEntry = CTkEntry(OptionsGroup, width=108, height=25, corner_radius=0, font=EntryFont,
                           placeholder_text="brightness: 0")
FpsEntry = CTkEntry(OptionsGroup, width=40, height=25, corner_radius=0, font=EntryFont, placeholder_text="fps")
InvertSwitch = CTkSwitch(OptionsGroup, font=EntryFont, text="Invert Color", fg_color=WINDOW_COLOR)
EncodeButton = CTkButton(OptionsGroup, command=lambda: start_encode(ProgressBar, StatusLabel),
                         text="start", width=65,
                         height=35, corner_radius=0,
                         fg_color="#FFFFFF", text_color="#000000", hover_color="#999999", font=PathLabelFont)
ProgressBar = CTkProgressBar(OptionsGroup, width=root.winfo_width() - 130, height=10, mode="determinate",
                             progress_color="#6DCA6B", fg_color=WINDOW_COLOR)
ProgressBar.configure(progress_color=WINDOW_COLOR)
ProgressBar.set(0)

StatusLabel = CTkLabel(OptionsGroup, font=EntryFont, text=status)

WidthEntry.bind("<FocusOut>", lambda event: calculate_height(WidthEntry, HeightLabel, CharacterWarning))
WidthEntry.bind("<Return>", lambda event: calculate_height(WidthEntry, HeightLabel, CharacterWarning))



VideoPathGroup.pack(expand=False, fill=NONE, side=TOP, pady=10, ipady=5)
VideoPathLabel.place(relx=0.4, rely=0.08)
VideoPathEntry.place(relx=0.10, rely=0.45)
VideoPathBrowse.place(relx=0.80, rely=0.45)

ExportPathGroup.pack(expand=False, fill=NONE, side=TOP, pady=0, ipady=5)
ExportPathLabel.place(relx=0.43, rely=0.08)
ExportPathEntry.place(relx=0.10, rely=0.45)
ExportPathBrowse.place(relx=0.80, rely=0.45)

OptionsGroup.pack(expand=True, fill=Y, side=TOP, pady=10)
CharacterWarning.place(relx=0.08, rely=0.3)
TitleEntry.place(relx=0.03, rely=0.09)
SizeFrame.place(relx=0.69, rely=0.09)
WidthEntry.pack(side=LEFT, expand=FALSE, padx=5)
XLabel.pack(after=WidthEntry, side=LEFT)
HeightLabel.pack(after=XLabel, side=LEFT, padx=10)
ContrastEntry.place(relx=0.7, rely=0.25)
BrightnessEntry.place(relx=0.7, rely=0.4)
FpsEntry.place(relx=0.7, rely=0.55)
InvertSwitch.place(relx=0.7, rely=0.7)
EncodeButton.place(relx=0.1, rely=0.6)
ProgressBar.place(relx=0.06, rely=0.86)
StatusLabel.place(relx=0.44, rely=0.7)

root.mainloop()
