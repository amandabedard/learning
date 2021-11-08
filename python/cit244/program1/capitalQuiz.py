"""
Capital Quiz
Amanda Bedard
September 10, 2021

This program will take a file with countries and capital cities, compose a dict with it,
and quiz the user on them for as many times as they wish, until they enter 'stop'
"""
import random

# Global declarations
# This stores the location of the file to be used for the countries and capitals
FILE_LOCATION = "./countries_and_capitals.txt"

"""
The main function, which orchestrates the execution of the capital quiz. Steps of execution
are outlined in comments below.
"""
def main ():
    # Step 1 - Turn the file data into a dict we can use for the quiz
    capitalDict = populateCapitalDict()

    # Step 2 - Begin the quiz! Return the number correct and incorrect after the user is done
    correctAnswers, incorrectAnswers = beginQuiz(capitalDict)

    # Step 3 - Print the user's score after they have finished the quiz
    print (f"You have finished your quiz! You got {correctAnswers} values correct and {incorrectAnswers} values incorrect")

"""
This function pulls data from the file location to populate the dict for the quiz
Returns: the dict of countries and capitals
"""
def populateCapitalDict():
    # The initially empty dict to store the countries and capitals
    capitalDict = {}
    # The file we plan to parse
    capitalFile = open(FILE_LOCATION)

    for line in capitalFile:
        # We will split on the first tab (due to some country names having spaces) and clear the extra whitespace from the capital
        country, capital = line.split("\t", 1)
        capital = capital.strip()
        capitalDict[country] = capital

    return capitalDict

"""
This function takes a dict and uses it to quiz the user until they wish to stop
Args:
  capitalDict: a dict of the countries and their capitals
Returns: the correct and incorrect answers
"""
def beginQuiz(capitalDict):
    # The variable to keep our quiz active
    continueQuiz = True
    # The counter for correct and incorrect answers
    correctAnswers = 0
    incorrectAnswers = 0
    # Generating a list of countries for use with random.choice
    countryList = list(capitalDict.keys())

    # Looping until the user decides to stop the quiz
    while continueQuiz:
        # Here, we select a random country from the list
        country = random.choice(countryList)
        # Prompt for input
        capitalInput = input(f"What is the capital of {country}?\nType 'STOP' to end the quiz: \n")

        # Check if the user wants to stop, if they are correct, or if they are incorrect
        if capitalInput.upper() == 'STOP':
            continueQuiz = False
        elif capitalInput == capitalDict[country]:
            correctAnswers += 1
        else:
            incorrectAnswers += 1
    # Loop has ended-- let's tell the user how they did!
    return correctAnswers, incorrectAnswers

# Calling the main function so the file can be run with ".\capitalQuiz.py"
main()
    