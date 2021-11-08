"""
Sort Efficency
Amanda Bedard
November 5, 2021

This program runs a bubble sort and selection sort
and compares the number of loops and swaps. This program
is  paired with a report on my findings
"""
import random
import re

DEFAULT_NUM_OF_NUMS = '1000'

"""
This is the bubble sort function
I had to modify some of the values differently from what was 
represented in the psuedocode because it was not fully 
sorting the list.
Returns: the counters for loops and swaps
"""
def bubbleSort(numList):
    # Variables for loop and swap counts, along with listSize
    listSize = len(numList)
    loopCount = 0
    swapCount = 0
    # Looping to listSize - 1 to sort every element
    for index in range(listSize - 1):
        # Sorting with the values next to each other
        for position in range(listSize - index - 1):
            loopCount += 1
            # If the value is greater than the one next to it, we swap
            if numList[position] > numList [position + 1]:
                swapCount += 1
                newNum = numList[position]
                numList[position] = numList[position + 1]
                numList[position + 1] = newNum
    # Return the number of loops and swaps
    return loopCount, swapCount

"""
This is the selection sort function
I had to modify some of the values differently from what was 
represented in the psuedocode here as well because it was not fully 
sorting the list.
Returns: the counters for loops and swaps
"""
def selectionSort(numList):
    loopCount = 0
    swapCount = 0
    # Starting at the beginning
    for startScan in range(len(numList)):
        index = startScan
        minIndex = startScan
        minValue = numList[startScan]

        # We are looking for the smallest value
        for index in range(startScan + 1, len(numList)):
            loopCount += 1
            # If it is the smallest value yet, we take note
            if numList[index] < minValue:
                minValue = numList[index]
                minIndex = index
        # We have gone through everything. Swap the smallest with the current.
        numList[minIndex] = numList[startScan]
        numList[startScan] = minValue
        swapCount += 1
    # Return the number of loops and swaps
    return loopCount, swapCount

"""
This function validates the user input against a regular expression.
Returns: a string value between 10-20000
"""
def validateUserNum(userNum):
    # This regular expression works with numbers 10-20000 and the text 'choose for me'
    validateExp = r"^([1-9][0-9][0-9]?[0-9]?|1[0-9][0-9][0-9][0-9]|20000|choose for me)$"
    # If the first request was choose for me, we default right away for efficency
    if userNum == 'choose for me':
        return DEFAULT_NUM_OF_NUMS
    else:
        # While the input is invalid, we will keep prompting
        while (not re.match(validateExp, userNum)):
            userNum = validateUserNum(input(f"Invalid input, enter a number between 10 and 20000 or say 'choose for me': "))
            if userNum == 'choose for me':
                # Set usernum to the default on choose for me so that we break the loop
                userNum = DEFAULT_NUM_OF_NUMS
        # Send the number string back to the user
        return userNum

"""
This function formats and prints the results of the sorting. If called
with no parameters, it will print the header columns.
"""
def formatAndPrintResults(sortName='ALGORITHM', loopCount='LOOP COUNT', swapCount='DATA MOVEMENT'):
    # Set up what we would like to print and print with correct formatting
    printRow = [sortName, loopCount, swapCount]
    print("{: <9}{: >20}{: >20}".format(*printRow))

"""
The main function. Gathers the number of numbers, fills the list with integers, executes the
two sorting algorithms, and prints the results.
"""
def main():
    # We have the lists for bubble and selection sort
    # along with loop and swap counters for each
    numListBubble = []
    numListSelection = []
    bubbleLoopCount = 0
    selectionLoopCount = 0
    bubbleSwapCount = 0
    selectionSwapCount = 0

    # We are calling the validateUserNum function on initial input, and casting the result
    # as an integer
    userNumOfNumbers = int(validateUserNum(input(f"How many numbers should be generated: \n")))

    # per instructions, populate the list with a 'for' loop
    for count in range(userNumOfNumbers):
        # Appending a random int between 0 and the max number
        numListBubble.append(random.randint(0,userNumOfNumbers))

    # Copying the list with a function because python sets variables with a reference
    numListSelection = numListBubble.copy()

    # We are executing the two sorts here and storing the number of loops and swaps
    bubbleLoopCount, bubbleSwapCount = bubbleSort(numListBubble)
    selectionLoopCount, selectionSwapCount = selectionSort(numListSelection)
    
    # Printing output here with formatting
    print('SORT ALGORITHM RUN EFFICENCY')
    formatAndPrintResults()
    formatAndPrintResults('Bubble', bubbleLoopCount, bubbleSwapCount)
    formatAndPrintResults('Selection', selectionLoopCount, selectionSwapCount)

main()



