import json
import sys
import re

#Define a data structure and file path
filePath = "./Quiz/data.json"
data = [
    {
        "question": "Where were the 2016 Summer Olympics held?",
        "answers": ["rio de janeiro", "rio", "brazil"],
        "difficulty": 2,
        "correct": 2,
        "incorrect": 1
    },
    {
        "question": "What is the unit code of Programming Principles?",
        "answers": ["csp1150"],
        "difficulty": 1,
        "correct": 0,
        "incorrect": 0
    }
]

def saveData(data, filePath):
    #Try to open the file if failure is met notify the user
    if askYesOrNo("Would you like to save your changes?"):  
        try:
            with open(filePath, "w") as file:
                json.dump(data, file, indent=4)         
                print("Your changes have been saved")
        except Exception as e:
            print(f"An error occurred while saving the data: {e}")

def openData(data, filePath):
    #Try to open the file if failure is met handle the error
    try:
        with open(filePath, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
        handleFileError(e, data, filePath)


def handleFileError(e, data, filePath):
    #Nofity the user of the problem
        print(f"An errror occured while trying to open the data file: {e}")
        
        #ask the user if they would like to create a new file
        if askYesOrNo("Would you like to create a new data file?"):
            saveData(data, filePath)
            openData(data,filePath)
        else:
            applicationQuit(filePath)
    

def applicationQuit():
    if (askYesOrNo("Are you sure you want to quit?")):
        print("Goodbye!")
        sys.exit()


def createNewQuestion():
    #Create a new question
    newQuestion = {
        "question": "",
        "answers": [],
        "difficulty": 0,
        "correct": 0,
        "incorrect": 0
        }
    
    #Get question from user
    newQuestion["question"] = inputString("Please enter a question: ") 
 
    #repeatedly ask if the user wants to add another answer
    print("Please enter all possible answers")
    addingAnswers = True
    while(addingAnswers):
        newQuestion["answers"].append(inputString("Please enter an answer: "))
        addingAnswers = askYesOrNo("Would you like to add another answer?")

    newQuestion["difficulty"] = inputInt("Please enter a number between 1-3: ", 3)

    return newQuestion

def askYesOrNo(prompt):
    return input(f"{prompt} (Y/N): ").lower() == "y"

def inputInt(prompt, max_value):
    #Purify the entered value to get the correct integer value
    value = 0
    while value == 0 or value > max_value or value < 0:
        try: 
            value = int(input(prompt))
        except ValueError as e:
            print(f"Please enter a number{e}")
    return value

def inputString(prompt):
    #Get a non empty string from the user input
    value = " "
    while value.isspace():
       value = input(prompt)
    return value

def listQuestions():
    #List the questions 
    index = 0
    for question in data:
        value = question["question"]
        #add 1 to the index to improve readability for the user
        print(f"[{index + 1 }] {value}")
        #itterate the index
        index += 1
          
def searchQuestions():
    if DataIsEmpty(): return
    
    term = inputString("Please enter a word in the question: ")

    foundQuestion = False
    #Loop through questions and 
    for question in data:
        value = question["question"]
        #find the string containing the search term 
        #make sure both strings have been set to lower case
        if re.search(term.lower(), value.lower()): 
            printWholeQuestion(question)
            foundQuestion = True

    if not foundQuestion:
        print("No Question Found")
            
def findQuestionByIndex():
    #Get index from user 
    if DataIsEmpty(): return
    
    index = inputInt(f"Please enter a number between 1-{len(data)}: ", len(data))
    #make the index is array useable with -=1
    index -= 1

    printWholeQuestion(data[index])
    
def printWholeQuestion(question):
    for key, value in question.items():
        print(f"{key} : {value}")

def deleteQuestion():
    #First list the questions
    listQuestions()
    #prompt the user to enter the index of the question to delete
    index = inputInt(f"Please enter a number between 1-{len(data)}: ", len(data))
    #make the index is array useable with -=1
    index -= 1
    #remove it from data
    questionName = data[index]["question"]
    if askYesOrNo(f"Are you sure you want to delete the question : {questionName}"):
        data.remove(data[index])
        print("Question has been deleted")
        saveData(data,filePath)

def addQuestion():
    data.append(createNewQuestion())
    saveData(data,filePath)

def quit():
    saveData(data,filePath)
    applicationQuit()

def DataIsEmpty():
    if len(data) == 0:
        print("Question list is empty, please add a questions with (a)")
        return True
    return False


print('Welcome to the Quiz Admin Program.')
data = openData(data, filePath)

while True:
    print('\nChoose [a]dd, [l]ist, [s]earch, [v]iew, [d]elete or [q]uit.')
    choice = input('> ').lower() 
    
    if choice == 'a':
        addQuestion()
    elif choice == 'l':
        listQuestions()
    elif choice == 's':
        searchQuestions()
    elif choice == 'v':
        findQuestionByIndex()
    elif choice == 'd':
        deleteQuestion()
    elif choice == 'q':
        quit()
    else:
        print("Invalid choice, please try again")


# If you have been paid to write this program, please delete this comment.
