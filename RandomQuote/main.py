# -*- coding: utf8 -*-
import random as r
import json
import scrapy
import subprocess


def readDataFromJson(fileName, key):
    """
    Returns a list with the data from a JSON file

    Parameters
    ----------
    fileName: the name of the json file to get data from (str)
    key: type of data inside json (str)

    Returns
    -------
    data: list of JSON content (list)

    Notes
    -----
    the key depends on the JSON file chosen.
    """
    data = []

    # Get the data from the file
    with open(fileName) as jFile:
        content = json.load(jFile)

        # Get eveything inside json file
        for entry in content:
            data.append(entry[key])
    
    return data


def getRandomItem(itemsList):
    """
    Function that returns a random item from a given list of items.

    Parameters
    ----------
    itemsList: list of items in which we select (list)

    Returns
    -------
    item: random item inside itemsList (str)

    """
    # Get a random index in range of the length of the list of items
    randInd = r.randint(0, len(itemsList) - 1)

    # Get item at random position given and return it
    item = itemsList[randInd]
    return item


def getRandomCharacter():
    """
    Returns a random character name.

    Returns
    -------
    name: the name of the random character (str)
    """
    # Get the list of characters
    charList = readDataFromJson("characters.json", "character")

    # Get random name and return it
    name = getRandomItem(charList)
    return name


def getRandomQuote():
    """
    Returns a random quote.

    Returns
    -------
    quote: the random quote (str)
    """
    # Get the list of quotes
    QuotesList = readDataFromJson("quotes.json", "quote")

    # Get random quote and return it
    quote = getRandomItem(QuotesList)
    # Clean quote
    quote = quote.strip().capitalize()
    return quote


def displayRandomSentence():
    """
    Display a random sentence (random char and quote)
    """
    # Get char and quote
    character = getRandomCharacter()
    quote = getRandomQuote()

    # Display final sentence
    print("{} a dit: {}.\n".format(character, quote))


def mainFunction():
    """
    Main function of script
    """
    # Define stop variable for loop
    keepGoing = True
    # Loop
    while keepGoing:
        # Display a random sentence
        displayRandomSentence()

        # Ask user what he wants to do
        choice = input("Voulez-vous voir une autre citation?"
                       " Pour sortir, tapez [B].\n>>> ").upper()
        
        # Change stop variable to stop the loop
        if choice == "B":
            keepGoing = False

# When program is directly called
if __name__ == "__main__":
    # Empty files with quotes and characters
    file = open("characters.json", "r+")
    file.truncate(0)
    file.close()
    file = open("quotes.json", "r+")
    file.truncate(0)
    file.close()

    subprocess.run(["scrapy", "runspider", "charSpider.py", "-o", "characters.json"])
    subprocess.run(["scrapy", "runspider", "quotesSpider.py", "-o", "quotes.json"])
    mainFunction()