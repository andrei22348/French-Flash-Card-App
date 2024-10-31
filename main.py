import os
import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}

if os.path.exists('data/not_learned_words.csv'):
    data = pandas.read_csv('data/not_learned_words.csv')
else:
    data = pandas.read_csv('data/french_words.csv')
    data.to_csv('data/not_learned_words.csv', index=False)

data_dict = data.to_dict(orient="records")
data1_dict = data_dict.copy()

def update_csv():
    updated_data = pandas.DataFrame(data1_dict)
    updated_data.to_csv('data/not_learned_words.csv', index=False)

def reset_data():
    global data1_dict
    data = pandas.read_csv('data/french_words.csv')
    data_dict = data.to_dict(orient="records")
    data1_dict = data_dict.copy()
    update_csv()

def next_card_red():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    if len(data1_dict) > 0:
        current_card = random.choice(data1_dict)
        canvas.itemconfig(canvas_image, image=image1)
        canvas.itemconfig(card_title, text='French', fill="black")
        canvas.itemconfig(card_word, text=current_card['French'], fill="black")
        flip_timer = window.after(3000, change_face)
    else:
        reset_data()
        next_card_red()
    print(data1_dict)
    print(len(data1_dict))


def next_card_green():
    global current_card, flip_timer
    window.after_cancel(flip_timer)

    if current_card in data1_dict:
        data1_dict.remove(current_card)
        update_csv()

    if len(data1_dict) > 0:
        current_card = random.choice(data1_dict)
        canvas.itemconfig(canvas_image, image=image1)
        canvas.itemconfig(card_title, text='French', fill="black")
        canvas.itemconfig(card_word, text=current_card['French'], fill="black")
        flip_timer = window.after(3000, change_face)
    else:
        reset_data()
        next_card_red()
    print(data1_dict)
    print(len(data1_dict))


def change_face():
    canvas.itemconfig(canvas_image, image=image2)
    canvas.itemconfig(card_title, text='English', fill="white")
    canvas.itemconfig(card_word, text=current_card['English'], fill="white")


window = Tk()
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, change_face)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
image1 = PhotoImage(file='images/card_front.png')
image2 = PhotoImage(file='images/card_back.png')
canvas_image = canvas.create_image(400, 263, image=image1)
card_title = canvas.create_text(400, 150, text='Title', font=('Ariel', 30, 'italic'))
card_word = canvas.create_text(400, 263, text='Word', font=('Ariel', 50, 'bold'))
canvas.grid(column=0, row=0, columnspan=2)

red_button_image = PhotoImage(file="images/wrong.png")
red_button = Button(image=red_button_image, highlightthickness=0, command=next_card_red)
red_button.grid(column=0, row=1)
red_button.config(borderwidth=0)

green_button_image = PhotoImage(file="images/right.png")
green_button = Button(image=green_button_image, highlightthickness=0, command=next_card_green)
green_button.grid(column=1, row=1)
green_button.config(borderwidth=0)

next_card_red()

window.mainloop()
