BACKGROUND_COLOR = "#B1DDC6"
import tkinter as tk
import pandas as pd
import random
import time
import json


data = pd.read_csv("data/french_words.csv")
data_list = data.to_dict(orient="records")

window = tk.Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50, bg = BACKGROUND_COLOR)

canvas = tk.Canvas(width=800, height=526)
card_front_img = tk.PhotoImage(file = "images/card_front.png")
card_back_img = tk.PhotoImage(file = "images/card_back.png")
incorrect_button_image = tk.PhotoImage(file = "images/wrong.png")
correct_button_image = tk.PhotoImage(file = "images/right.png")
background = canvas.create_image(400, 263, image = card_front_img)
tittle_text = canvas.create_text(400, 150, text = "Tittle", font = ("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 250, text = "Word", font = ("Ariel", 60, "italic"))
canvas.grid(column=0, row = 0, columnspan=2)
canvas.config(bg = BACKGROUND_COLOR, highlightthickness=0)
    
def flip_card(card):
    '''Fucntion which flips card from french to english word.'''
    word_english = card["English"]
    canvas.itemconfig(background, image = card_back_img )
    canvas.itemconfig(tittle_text, text = "English", fill = "black")    
    canvas.itemconfig(word_text, text = word_english, fill = "black") 
    
def next_card():
    '''Function which chooses one dictionary from list data_list and 
        updating the canvas with given word.'''
    global card, word_french
    card = random.choice(data_list)
    word_french = card["French"]
    canvas.itemconfig(background, image = card_front_img )
    canvas.itemconfig(tittle_text, text = "French", fill = "black")    
    canvas.itemconfig(word_text, text = f"{word_french}", fill = "black") 
    canvas.update_idletasks()
    time.sleep(3)
    
    flip_card(card)
    
    
def click(string):
    '''Function which stores data in .json file. '''
    
    if string == "correct":
        key = "Known_words"
    else:
        key = "Unknow_words"
        
    try:
        with open("Words.json", "r") as data_file:
            data = json.load(data_file)
            
            if key in data:
                if word_french not in data[key]:
                    data[key].append(word_french)
                else:
                    pass
            else:
                data[key] = [word_french]
                
    except FileNotFoundError:
        print("File Words.json not found!")
        with open("Words.json", "w") as data_file:
            data = {key:[word_french]}
            json.dump(data, data_file)
    else:
        with open("Words.json", "w") as data_file:
            json.dump(data, data_file, indent=4)  
    
    next_card()
    
incorrect_button = tk.Button(image=incorrect_button_image, command = lambda: click("incorrect"))
incorrect_button.grid(row = 1, column=0)
correct_button = tk.Button(image = correct_button_image, command=lambda:click("correct"))
correct_button.grid(row=1, column=1) 

  
window.after(5000, next_card)
window.mainloop()    
    



