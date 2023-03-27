import tkinter.ttk as ttk
import tkinter as tk
import ttkthemes as ThemedStyles
import time
import sys
import os

class Pomodoro(ttk.Frame):

    onTop = False
    timerSeconds = 0        
    timeTitleText = ""
    timerStarted = False
    timerRunning = False
    timerTask = None
    notifyOnComplete = False
    style = None

    darkMode = False

    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def startTimer(self, minutes):
        self.timerSeconds = int(minutes) * 60
        self.timeTitle.config(text=self.timeTitleText)
        self.timeDisplay.config(text="00:00")
        self.updateTimer()

    def updateTimer(self):
        if not self.timerRunning:
            # cancel the timer task
            self.parent.after_cancel(self.timerTask)
            return
        if self.timerSeconds > 0:
            self.timerSeconds -= 1
            self.timeDisplay.config(text=time.strftime("%M:%S", time.gmtime(self.timerSeconds)))
            self.timerTask = self.parent.after(1000, self.updateTimer)
        else:
            if self.notifyOnComplete:
                # Notify the user that the time is up
                self.parent.bell()
                # Make the window always on top
                self.parent.call('wm', 'attributes', '.', '-topmost', '1')
                # Make the window always on top as set by the user
                self.parent.after(1000, lambda: self.parent.call('wm', 'attributes', '.', '-topmost', '1' if self.onTop else '0'))
                # Change the background color back to normal
                self.parent.after(1000, lambda: self.parent.config(bg="SystemButtonFace"))


            if self.timeTitleText == "Productivity Phase":
                self.timeTitleText = "Break Phase"
                seconds = 0
                try:
                    seconds = int(self.breakTime.get())
                except ValueError:
                    seconds = 25
                self.startTimer(seconds)
            else:
                self.timeTitleText = "Productivity Phase"
                minutes = 0
                try:
                    minutes = int(self.productivityTime.get())
                except ValueError:
                    minutes = 25
                self.startTimer(minutes)

    def start(self):
        if self.timerRunning:
            return
        self.timeTitleText = "Productivity Phase"
        self.pauseButton.config(text="Pause")
        self.timerRunning = True
        self.timerStarted = True
        minutes = 0
        try:
            minutes = int(self.productivityTime.get())
        except ValueError:
            minutes = 25
        self.startTimer(minutes)

    def togglePause(self):
        if self.timerRunning:
            self.timerRunning = False
            self.parent.after_cancel(self.timerTask)
            self.timeTitle.config(text="Paused")
            self.pauseButton.config(text="Resume")
        elif self.timerStarted:
            self.timeTitle.config(text=self.timeTitleText)
            self.pauseButton.config(text="Pause")
            self.timerRunning = True
            self.updateTimer()


    def stop(self):
        self.timerRunning = False
        self.timerStarted = False
        self.pauseButton.config(text="Pause")
        self.timeTitle.config(text="Productivity Phase")
        self.timeDisplay.config(text="00:00")
    
    def toggleAlwaysOnTop(self):
        self.onTop = not self.onTop
        self.parent.call('wm', 'attributes', '.', '-topmost', '1' if self.onTop else '0')

    def toggleNotifyOnComplete(self):
        self.notifyOnComplete = not self.notifyOnComplete

    def toggleDarkMode(self):
        self.darkMode = not self.darkMode
        if self.darkMode:
            self.style.set_theme("equilux")
        else:
            self.style.set_theme("arc")

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self.parent.title("Pomodoro Timer")
        self.parent.geometry("350x250")
        self.parent.wm_iconbitmap(default=Pomodoro.resource_path("resources/icon.ico"))
        self.parent.resizable(0,0)

        self.style = ThemedStyles.ThemedStyle(self.parent)
        self.style.set_theme("arc")

        self.mainFrame = ttk.Frame(self.parent)

        self.label = ttk.Label(self.mainFrame, text="Pomodoro Timer", font=("Arial", 20))
        self.label.pack()

        # Add a big space between the label and the buttons
        self.spacer1 = ttk.Label(self.mainFrame, text="")
        self.spacer1.pack()


        self.timeFrame = ttk.Frame(self.mainFrame)

        # Create a input for minutes for productivity and break
        self.productivityLabel = ttk.Label(self.timeFrame, text="Productivity Time")
        self.productivityLabel.pack(side="left")
        self.productivityTime = ttk.Entry(self.timeFrame, width=5, validate="key", validatecommand=(self.parent.register(lambda P: P.isdigit() and int(P) > 0 and int(P) <= 60 or P == ""), '%P'))
        self.productivityTime.insert(0, "25")
        self.productivityTime.pack(side="left")

        self.breakLabel = ttk.Label(self.timeFrame, text="Break Time")
        self.breakLabel.pack(side="left")

        self.breakTime = ttk.Entry(self.timeFrame, width=5, validate="key", validatecommand=(self.parent.register(lambda P: P.isdigit() and int(P) > 0 and int(P) <= 60 or P == ""), '%P'))
        self.breakTime.insert(0, "5")
        self.breakTime.pack(side="left")
        
        self.timeFrame.pack()

        self.spacer2 = ttk.Label(self.mainFrame, text="")
        self.spacer2.pack()

        self.timeTitle = ttk.Label(self.mainFrame, text="Productivity Phase", font=("Arial", 20))
        self.timeTitle.pack()

        self.timeDisplay = ttk.Label(self.mainFrame, text="00:00", font=("Arial", 20))
        self.timeDisplay.pack()

        self.checkBoxFrame = ttk.Frame(self.mainFrame)
        self.alwaysOnTopCheckbox = ttk.Checkbutton(self.checkBoxFrame, text="Always on Top", command=self.toggleAlwaysOnTop)
        self.alwaysOnTopCheckbox.state(['!alternate'])
        self.alwaysOnTopCheckbox.pack(side="left")
        self.notifyOnCompleteCheckbox = ttk.Checkbutton(self.checkBoxFrame, text="Notify on Complete", command=self.toggleNotifyOnComplete)
        self.notifyOnCompleteCheckbox.state(['!alternate'])
        self.notifyOnCompleteCheckbox.pack(side="left")

        self.checkBoxFrame.pack()

        self.darkModeCheckbox = ttk.Checkbutton(self.mainFrame, text="Dark Mode", command=self.toggleDarkMode)
        self.darkModeCheckbox.state(['!alternate'])
        self.darkModeCheckbox.pack()

        self.buttonFrame = ttk.Frame(self.mainFrame)
        self.startButton = ttk.Button(self.buttonFrame, text="Start", command=self.start)
        self.startButton.pack(side="left")
        self.pauseButton = ttk.Button(self.buttonFrame, text="Pause", command=self.togglePause)
        self.pauseButton.pack(side="left")

        self.stopButton = ttk.Button(self.buttonFrame, text="Stop", command=self.stop)
        self.stopButton.pack(side="left")

        self.buttonFrame.pack()
        
        self.mainFrame.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    Pomodoro(root).pack(side="top", fill="both", expand=True)

    root.mainloop()
