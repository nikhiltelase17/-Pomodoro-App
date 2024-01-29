from tkinter import *
import math
import win32com.client
import pygame

speaker = win32com.client.Dispatch("SAPI.SpVoice")
pygame.mixer.init()
click_sound = pygame.mixer.Sound("click_effect-86995.mp3")

# Constants for colors, font, and time intervals
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0  # Counter for work/break repetitions
timer = None  # Handle for the active timer


def reset_timer():
    '''Function to reset the timer and UI elements'''
    global reps
    global timer

    pygame.mixer.Sound.play(click_sound)

    window.after_cancel(timer)  # Cancel running timer
    title_label.config(text="Timer")
    check_label.config(text="")
    canvas.itemconfig(timer_text, text="00:00")  # Reset timer text
    reps = 0  # Reset rep count



def start_timer():
    '''Function to start the timer based on work/break cycles'''
    global reps
    reps += 1  # Increment rep count
    pygame.mixer.Sound.play(click_sound)

    work_seconds = WORK_MIN * 60  # Convert work minutes to seconds
    short_break_seconds = SHORT_BREAK_MIN * 60  # Convert short break minutes to seconds
    long_break_seconds = LONG_BREAK_MIN * 60  # Convert long break minutes to seconds

    if reps % 8 == 0:
        # Long break after every 8 reps
        speaker.Speak("time to long break")
        title_label.config(text="Break", fg=RED)
        count_down(long_break_seconds)
    elif reps % 2 == 0:
        speaker.Speak("time to short break")
        # Short break after every 2 reps
        title_label.config(text="Break", fg=PINK)
        count_down(short_break_seconds)
    else:
        # Work session
        speaker.Speak("time to work")
        title_label.config(text="Work", fg=GREEN)
        count_down(work_seconds)


def count_down(count):
    '''Function to handle the countdown and display the remaining time'''
    count_min = math.floor(count / 60)  # Calculate minutes
    count_sec = count % 60  # Calculate seconds

    # Format time with leading zeros
    if count_min < 10:
        count_min = f"0{count_min}"
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")  # Update timer text

    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)  # Reschedule timer after 1 second
    else:
        start_timer()  # Start the next cycle
        mark = ""
        work_sessions = math.floor(reps / 2)  # Calculate completed work sessions
        for _ in range(work_sessions):
            mark += "✅"  # Add checkmarks for completed work sessions
        check_label.config(text=mark)  # Display checkmarks


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro App")
window.config(padx=100, pady=50, background=YELLOW)
# Load image resources
tomato_img = PhotoImage(file="tomato.png")
start_img = PhotoImage(file="icons8-start-30 (1).png")
reset_img = PhotoImage(file="icons8-reset-30.png")

title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 35, "bold"))
title_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, background=YELLOW)
canvas.create_image(102, 111, image=tomato_img)
timer_text = canvas.create_text(102, 130, text="00:00", fill="white", font=(FONT_NAME, 30, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", image=start_img, compound=LEFT, command=start_timer, font=(FONT_NAME, 10, "bold"))
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", image=reset_img, compound=LEFT, command=reset_timer, font=(FONT_NAME, 10, "bold"))
reset_button.grid(column=2, row=2)

check_label = Label(text="")
check_label.grid(column=1, row=3)

window.mainloop()
