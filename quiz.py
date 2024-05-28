# Import the necessary module(s).
import tkinter, tkinter.messagebox, random, json

class ProgramGUI:

    def __init__(self):
        self.filePath = "./Quiz/data.json"
        self.data = self.openData()

        self.answeredQuestions = []
        self.currentQuestion = self.getQuestion()
        self.currentQuestionNumber = 1
        self.maxQuestions = 5
        self.totalCorrect = 0

        if self.checkQuestionAmount() == False:
            self.applicationQuit()

        #Open main window
        self.main = tkinter.Tk()
        self.main.title("Quiz")
        self.main.geometry("300x100")
        
        #Create labels
        self.QuestionNumber = tkinter.Label(self.main, text=f"Question {self.currentQuestionNumber} of {len(self.data)}")
        self.QuestionNumber.pack(side='top')

        self.Question = tkinter.Label(self.main, text=self.currentQuestion["question"])
        self.Question.pack()

        self.QuestionDifficulty = tkinter.Label(self.main, text="Difficulty: " + str(self.currentQuestion["difficulty"]) + "/3")
        self.QuestionDifficulty.pack()

        #Create Frame for answer entry and submit button
        self.frame = tkinter.Frame(self.main, padx='8',pady='8')
        self.frame.pack(side='bottom')
        self.submitButton = tkinter.Button(self.frame, text="Sumbit Answer", command=self.onSubmitAnswer)
        self.submitButton.pack(side='right')
        self.answer = tkinter.Entry(self.frame, text="Answer Entry")
        self.answer.pack(side='left')

        #Start tkinter to show window
        tkinter.mainloop()

    def openData(self):
        #Try to open the file if failure is met handle the error
        try:
            with open(self.filePath, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e: 
            tkinter.messagebox.showerror(f"An error occured while trying to open the data file: {e}")

    def checkQuestionAmount(self):
        if len(self.data) < 5:
            tkinter.messagebox.showerror("Error","Not enough questions")

    def onSubmitAnswer(self):
        if self.answerIsCorrect():
            #Notify the user if they are correct and add one to the total and question correct ints
            tkinter.messagebox.showinfo("Correct!", "You have entered a correct answer!")
            self.totalCorrect += 1
            self.currentQuestion["correct"] +=1
        else: 
            #Notify the user they are incorrect and add one to the current question incorrect int
            tkinter.messagebox.showerror("Incorrect!","You have entered an incorrect answer!")
            self.currentQuestion["incorrect"] +=1

        #itterate the question number
        self.currentQuestionNumber += 1

        #Update the UI
        if self.currentQuestionNumber  <= self.maxQuestions:
            self.QuestionNumber.config(text=f"Question {self.currentQuestionNumber} of {len(self.data)}")

            self.answeredQuestions.append(self.currentQuestion)
            self.currentQuestion = self.getQuestion()

            self.QuestionDifficulty.config(text="Difficulty: " + str(self.currentQuestion["difficulty"]) + "/3")
            self.Question.config(text=self.currentQuestion["question"])

        else:
            tkinter.messagebox.showinfo("Quiz Complete!",f"You Scored: {self.totalCorrect}/{self.maxQuestions}")
            self.updateData()
            self.saveData()
            self.applicationQuit()

    def updateData(self):
        for dataItem in self.data:
            for answerItem in self.answeredQuestions:
                if dataItem["question"] == answerItem["question"]:
                    dataItem = answerItem

    def saveData(self):
    #Try to open the file if failure is met notify the user
        try:
            with open(self.filePath, "w") as file:
                json.dump(self.data, file, indent=4)
        except Exception as e:
            print(f"An error occurred while saving the data: {e}")

    def getQuestion(self):
        newQuestion = ""
        while newQuestion == "":
            newQuestion = self.getUniqueRandomQuestion()
        return newQuestion

    def getUniqueRandomQuestion(self):
        newQuestion = self.data[random.randrange(0,len(self.data))]
        if len(self.answeredQuestions) > 0:
            for item in self.answeredQuestions:
                if item["question"] == newQuestion["question"]:
                    return ""
        return newQuestion

    def answerIsCorrect(self):
        answer = self.answer.get()
        for item in self.currentQuestion["answers"]:
            if answer.lower() == item.lower():
                return True
        return False


    def applicationQuit(self):
        self.main.destroy()


# Create an object of the ProgramGUI class to begin the program.
gui = ProgramGUI()

# If you have been paid to write this program, please delete this comment.
