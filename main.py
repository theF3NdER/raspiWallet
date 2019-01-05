import json, io, os
import time
import datetime
from collections import namedtuple

parentExpense = namedtuple('parentExpense', 'id name')
childExpense = namedtuple('childExpense', 'parent name')

expenseParent = [parentExpense(1, 'House'), parentExpense(2, 'Food'), parentExpense(3, 'Fun'), parentExpense(4, 'Subscriptions'),
                parentExpense(5, 'Healthcare'), parentExpense(6, 'Gifts'), parentExpense(7, 'Transports'), parentExpense(8, 'Documents and Fees')]

expenseChild = [
                childExpense('House', ['rent', 'bills', 'maintenance', 'stuff']),
                childExpense('Food', ['grocery', 'takeaway', 'extra']),
                childExpense('Fun', ['alcol', 'events', 'hobbies', 'software', 'hardware']),
                childExpense('Subscriptions', ['voice', 'others']),
                childExpense('Healthcare', ['barbershop', 'cloth', 'doctor', 'medicines', 'soaps']),
                childExpense('Gifts', ['christmas', 'degrees', 'birthdays', 'love', 'friends', 'marriage']),
                childExpense('Transports', ['goingHome', 'trip', 'public', 'other']),
                childExpense('Documents and Fees', ['document', 'fee', 'fine', 'insurance'])
]

with open('/media/davide/D/Shared/Progetti/Raspino/Portafogli/incomeCategories.json') as f:
    incomeCategories = json.load(f)

with open('/media/davide/D/Shared/Progetti/Raspino/Portafogli/data.json') as z:
    outcome = json.load(z)

def makeExpense():
    print("What did you payed?\n\
            1.House\n\
            2.Food\n\
            3.Fun\n\
            4.Subscriptions\n\
            5.Healthcare\n\
            6.Gifts\n\
            7.Transports\n\
            8.Documents and Fees")
    choiseCat = int(input(":"))
    category = list(filter(lambda x: x.id==int(choiseCat), expenseParent))[0].name
    
    print("\n\nWhat it was?")
    children = (list(filter(lambda x: x.parent==category, expenseChild))[0].name)
    for childId in range(len(children)):
        print("\t"+str(childId+1)+"."+str(children[childId]))
    choiseWhat = int(input(":"))    
    what = expenseChild[choiseCat-1].name[choiseWhat-1]

    amount = input("\n\nHow much? ")

    print("\n\nWhen you payed it?")
    d = int(input("Insert day: "))
    date = datetime.datetime(int(datetime.datetime.now().strftime("%Y")), int(datetime.datetime.now().strftime("%m")), d)

    cause = input("\n\nWhat it was about?\n: ")

    mandatory = bool(input("\n\nWas it mandatory? (y/n)\n")=="y")

    note = input("\n\nAny notes?\n")

    return (category, what, amount, mandatory, date.strftime("%d-%m-%Y"), cause, note)


def addExpense(outcome, expense):
    dic = {
            'amount': expense[2],
            'mandatory': expense[3],
            'date': expense[4],
            'cause': expense[5],
            'note': expense[6]
    }

    outcome[expense[0]][expense[1]]['expenses'].append((dic))
    outcome[expense[0]][expense[1]]['totalOutcome'] = updateOutcomes(expense[0], expense[1])

    return outcome

def printDetails(parent, child, amount):
    pass


def storeJSON(data):
    with open('/media/davide/D/Shared/Progetti/Raspino/Portafogli/data.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

def updateOutcomes(parent, child):
    totalAmount = 0
    for expense in outcome[parent][child]['expenses']:
        totalAmount += float(expense['amount'])
    
    return totalAmount

def monthOutcome(month=datetime.datetime.now().strftime("%m")):
    totalAmount = 0.0
    for parent in [expense.name for expense in expenseParent]:
        for child in list(filter(lambda x: x.parent==parent, expenseChild))[0].name:
            for expense in outcome[parent][child]['expenses']:
                if(expense['date'].split('-')[1]==month):
                    totalAmount += float(expense['amount'])
    
    return totalAmount

def printOutcome():
    print("***This is the total report since the very beginning***\n")
    for parent in [expense.name for expense in expenseParent]:
        print(parent)
        for child in list(filter(lambda x: x.parent==parent, expenseChild))[0].name:
            for expense in outcome[parent][child]['expenses']:
                print('\t'+child+" ("+str(expense['cause'])+"): "+'%24s' %str(expense['amount']))
                # print('\t'+child+": "+str(expense['amount']))
            if len(outcome[parent][child]['expenses'])>0:
                print('\t--------')
                print('\t\t'+str(outcome[parent][child]['totalOutcome'])+'\n')
    print("\n")

def printMonthDetails(month=datetime.datetime.now().strftime("%m")):
    print("***This is the report for this month***\n")
    for parent in [expense.name for expense in expenseParent]:
        print('\n'+parent)
        for child in list(filter(lambda x: x.parent==parent, expenseChild))[0].name:
            monthChildOutcome = 0.0
            for expense in outcome[parent][child]['expenses']:
                if(expense['date'].split('-')[1]==month):
                    print('\t'+child+" ("+str(expense['cause'])+"):\t"+str(expense['amount']))
                    monthChildOutcome += float(expense['amount'])
            if expense['date'].split('-')[1]==month and len(outcome[parent][child]['expenses'])>0:
                print('\t--------')
                print('\t\t'+str(monthChildOutcome)+'\n')
    print("\n")

    totalAmount = monthOutcome()
    print("This month you spent: "+ str(totalAmount)+"€")

def nav():
    print("What you wanna do?\n\
            1.Add expense\n\
            2.Look at the monthly report\n\
            3.Look at the total report")
    choise = int(input(":"))

    if choise==1:
        expense = makeExpense()
        newOutcome = addExpense(outcome, expense)

        storeJSON(newOutcome)
    elif choise==2:
        printMonthDetails()
    elif choise==3:
        printOutcome()
    else:
        print("Invalid choise")


def main():
    nav()


if __name__ == '__main__':
    main()