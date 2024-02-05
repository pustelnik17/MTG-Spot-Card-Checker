import CardManager
import customtkinter as gui
from PIL import Image
import re

def Load():
    global text
    with open("data.txt", mode="r") as file:
        for element in file.readlines():
            inputText.insert('end', element)
        priceText.insert('end', "50")

def Search():
    result = inputText.get(0.0, "end").splitlines()
    for cardId in range(len(result)):
        result[cardId] = re.sub("^[0-9]* ", "", result[cardId])
    search = CardManager.Data(result, upperBound=float(priceText.get(0.0, "end")))
    sum = count = 0
    outputText.delete(0.0, "end")
    for card in search.result:
        if card["cost"] != -1:
            count += 1
            sum += float(card["cost"])
            outputText.insert("end", "[" + str(card["cost"]) + "] " + ((card["name"][:25] + '..') if len(card["name"]) > 25 else card["name"]) + "\n")
        else:
            outputText.insert("end", "[----] " + ((card["name"][:25] + '..') if len(card["name"]) > 25 else card["name"]) + "\n")
    summaryLabel.configure(text=f"{count} of {len(result)} | {round(sum, 2)} zł")
    myTab.set("Output")

def Save():
    with open("data.txt", mode="w") as file:
        file.write(inputText.get(0.0, "end"))

gui.set_appearance_mode("dark")
gui.set_default_color_theme("dark-blue")

root = gui.CTk()
root.geometry("400x1000+0+0")
root.title("MTG Spot Card Checker")

searchImage = gui.CTkImage(Image.open("resources/search.ico").resize((20, 20)))
saveImage = gui.CTkImage(Image.open("resources/save.ico").resize((20, 20)))


buttonFrame = gui.CTkFrame(root)
searchButton = gui.CTkButton(buttonFrame, image=searchImage, text="", width=90, command=Search)
saveButton = gui.CTkButton(buttonFrame, image=saveImage, text="", width=90, command=Save)
myTab = gui.CTkTabview(root)
inputTab = myTab.add("Input")
outputTab = myTab.add("Output")
inputText = gui.CTkTextbox(inputTab, font=("consolas", 14))
priceFrame = gui.CTkFrame(inputTab)
priceLabel = gui.CTkLabel(priceFrame, text="Max Per Card [zł]:", font=("consolas", 18))
priceText = gui.CTkTextbox(priceFrame, font=("consolas", 18), height=30, width=80)
outputText = gui.CTkTextbox(outputTab, font=("consolas", 14))
summaryLabel = gui.CTkLabel(outputTab, text="Summary", font=("consolas", 18))

Load()
buttonFrame.pack(pady=10, padx=40)
searchButton.grid(row=0, column=0, padx=10)
saveButton.grid(row=0, column=1, padx=10)
myTab.pack(fill="both", expand=True)
priceFrame.pack(pady=10, padx=40)
priceLabel.grid(row=0, column=0, padx=10)
priceText.grid(row=0, column=1, padx=10)
inputText.pack(pady=10, padx=40, fill="both", expand=True)
summaryLabel.pack(pady=10, padx=40, fill="x")
outputText.pack(pady=10, padx=40, fill="both", expand=True)

root.mainloop()