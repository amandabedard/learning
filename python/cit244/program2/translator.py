"""
French Translator
Amanda Bedard
October 1, 2021

This program allows the user to specify a french/english file to use
with a translator UI, with various (add, delete, save, etc) functions
"""
# tkinter and os imports for the program
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
import os

# Giving constant names to the pairs to make references clearer
ENGLISH = 0
FRENCH = 1

"""
The main function, which orchestrates the creation of the GUI object and starts
the tkinter mainloop.
"""
def main():
    gui = MyGUI()
    gui.ui.mainloop()

"""
This function uses a file path to open the specified file to get the translation data
Returns: the 2d list of translation pairs
"""
def readFile(filePath):
    # Opening with utf-8 encoding to preserve the special characters
    translateList = []
    translateFile = open(filePath, encoding="utf-8")

    for line in translateFile:
        # We will split on the first tab (due to some translations having spaces)
        # and clear whitespace
        english, french = line.split("\t", 1)
        french = french.strip()
        translateList.append([english, french])
    return translateList

class MyGUI:
    #####################################################################
    # Private helper methods for the class are listed below
    # These methods contain code that is reused throughout the program
    #####################################################################
    """
    This private function turns the 2d list of word pairs into a string
    Returns: a string of the 2d list
    """
    def __stringifyList(self):
        translationString = ""
        for pair in self.translateList:
            lineOfText = pair[ENGLISH] + "\t\t\t" + pair[FRENCH] + "\n"
            translationString= translationString + lineOfText
        
        return translationString
    """
    This private function saves the stringified 2d list to a file
    """
    def __saveToFile(self):
        # Gets the string list first
        translateData = self.__stringifyList()
        # Opens and overwrites the new data to the file
        with open(self.filePath, "w", encoding="utf-8") as file:
            file.write(translateData)
    """
    This private function generates the UI components
    I chose to abstract this from init because I wanted to keep it 
    short and limited in behavior.
    Returns: the ui object generated in the function
    """
    def __generateUi(self):
        # Getting the app ready with the initial object, title, column, and row settings
        ui = Tk()
        ui.title("  English to French Translator  ")
        ui.grid_columnconfigure(0, weight=1)
        ui.grid_rowconfigure(0, weight=1)
        
        # Creating the buttons and text boxes
        Label(ui, text="Display All:").grid(row=1, column=1, sticky=W, padx=(10, 0))
        # We want this to be read only so the user has confidence in the data integrity
        # Also adding a scroll bar to look nicer
        self.entireTextList = Text(ui, height = 10, width = 50,state=DISABLED)
        self.entireTextList.grid(column=1, row=2, columnspan=2, sticky='ew', padx=(10, 0))
        scrollb = Scrollbar(ui, orient='vertical', command=self.entireTextList.yview)
        scrollb.grid(row=2, column=3, sticky='ns')
        self.entireTextList.config(yscrollcommand=scrollb.set)
        # These labels aren't going to change so there is no need to assign them
        Label(ui, text = "English Text:").grid(row = 4, column = 1, sticky = W, padx=10)
        Label(ui, text = "French Text:").grid(row = 4, column = 2, sticky = W)
        # Edit-friendly text boxes for the English and French text and configurations
        self.english = Text(ui, height = 2, width = 25)
        self.english.grid(row = 5, column = 1, sticky = W, padx=10)
        self.french = Text(ui, height = 2, width = 25)
        self.french.grid(row = 5, column = 2, sticky = W, padx=(0, 10))
        # A nice little button for the translation to French functionality
        ttk.Button(ui, text="TRANSLATE", command=self.translateToFrench).grid(row=6, column = 1, pady=10)

        # Creating the menu items and mapping functions to them. Below is for 'File'
        menu = Menu(ui)
        fileMenu = Menu(menu, tearoff=0)
        fileMenu.add_command(label="Open", command=self.processOpen)
        fileMenu.add_command(label="Save", command=self.update)
        fileMenu.add_command(label="Exit", command=self.exit)
        menu.add_cascade(label="File", menu=fileMenu)
        # The items and functions below are corresponding to 'Edit'
        editMenu = Menu(menu, tearoff=0)
        editMenu.add_command(label="List Dictionary", command=self.displayAll)
        editMenu.add_command(label="Add Word", command=self.addWord)
        editMenu.add_command(label="Delete Word", command=self.deleteWord)
        menu.add_cascade(label="Edit", menu=editMenu)

        # Configure and return the UI object
        ui.config(menu=menu)
        return ui
    
    #####################################################################
    # The below methods are required for the program per the description
    # in order to complete the assignment
    #####################################################################
    """
    This function serves as the constructor for the MyGUI object.
    It initializes the UI object and translate list
    """
    def __init__(self):
        self.translateList = []
        self.ui = self.__generateUi()

    """
    This function gets the filepath from an open file widget and sends it through readFile
    to get the 2d list with data and sets it as an object property
    """
    def processOpen(self):
        # Display box to select file to open. 
        # Using this feature as read only because we're just getting the filename
        file = filedialog.askopenfile(mode='r')
        self.filePath = os.path.abspath(file.name)
        self.translateList = readFile(self.filePath)

    """
    This function takes the 2d list, stringifies the contents, then displays in a read only textbox
    """
    def displayAll(self):
        # Call this private function to get a stringified value for the list
        translationString = self.__stringifyList()
        
        # Changing the state to normal so we can update. Changing back after update.
        self.entireTextList.config(state=NORMAL)
        # Strip off the extra new lines and add to the window before disabling
        self.entireTextList.delete("1.0", END)
        self.entireTextList.insert(END, translationString.strip())
        self.entireTextList.config(state=DISABLED)

    """
    This function takes the English word (if any) in the textbox and finds a french match
    from the 2d list to display to the user
    """
    def translateToFrench(self):
        # Get the word from the text box and strip the newline
        englishWord = self.english.get("1.0", END).strip()
        frenchWord = ""
        self.french.delete("1.0", END)

        # Let's see if we can find the match
        # A little too long to do list comprehension and still be easily readable so we will write it normally
        for pair in self.translateList:
            if pair[ENGLISH] == englishWord:
                # We matched! Display the French word
                frenchWord += pair[FRENCH] + "\n"
                # Not breaking because we can have multiple matches

        # Adding the match(es) to the output sans the ending newline
        self.french.insert(END, frenchWord.strip())
    
    """
    This function takes the contents of the English and French textboxes and creates a new
    entry in the 2d list for the values
    """
    def addWord(self):
        # Get the contents of the textboxes and append word pair to 2d list
        englishWord = self.english.get("1.0", END).strip()
        frenchWord = self.french.get("1.0", END).strip()

        self.translateList.append([englishWord, frenchWord])

    """
    This function takes the entry from the English text box and deletes any matching French values
    from the 2d list
    """
    def deleteWord(self):
        # Using list comprehension, removing any matches from the list
        englishWord = self.english.get("1.0", END).strip()
        self.translateList = [pair for pair in self.translateList if not pair[ENGLISH] == englishWord]
        

    """
    This function will save the 2d list to file, and then clear every textbox on the ui
    """
    def update(self):
        # We are saving the file here with our private helper
        self.__saveToFile()

        # Now, to clear the data. We must enable the list all box but the others can just be cleared
        self.entireTextList.config(state=NORMAL)
        self.entireTextList.delete("1.0", END)
        self.entireTextList.config(state=DISABLED)

        self.english.delete("1.0", END)
        self.french.delete("1.0", END)

    """
    This function will save to file and then quit the UI
    """
    def exit(self):
        # Calling helper to save before exiting the UI
        self.__saveToFile()
        self.ui.quit()

# This allows us to run this as standalone code or a reusable module
if __name__ == "__main__":
    main()