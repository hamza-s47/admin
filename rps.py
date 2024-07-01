import random
import numpy as np

print ("Rock Paper Scissor\n".upper())

#Computer
compValues = np.array(['r','p', 's'])
scoreComp = 0

#Person
scorePerson = 0

while(scorePerson != 3 and scoreComp != 3):
    Randnum = random.randint(0, 2)
    compValues2 = compValues[Randnum]
    personInput = input("R/P/S: ")
    print("Computer has: ", compValues2)
    
    if personInput.lower() == compValues2:
            scoreComp += 1
            scorePerson += 1
    elif (personInput.lower() == 'r' and compValues2 == 's') or \
            (personInput.lower() == 'p' and compValues2 == 'r') or \
            (personInput.lower() == 's' and compValues2 == 'p'):
                scorePerson += 1
    else:
            scoreComp += 1
        
    print("\nYour score: ", scorePerson,)
    print("Computer score: ", scoreComp, "\n")
    
    if scoreComp == 3 and scorePerson < 3:
            print("\nYou lose🥲\n")
            break
    elif scoreComp <3 and scorePerson == 3:
            print("\nYou won🥳\n")
            break
    elif scoreComp == 3 and scorePerson == 3:
            print("\nMatch Tied🤯\n")
            break



