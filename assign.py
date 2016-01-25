import random
import csv
import base64 as b64

class Participant:
    def __init__(self,name,willShipTo,address,shipAnythingRemark,hints,isUSA=1):
        self.name = name
        self.willShipTo = willShipTo
        self.shipAnythingRemark = shipAnythingRemark
        self.hints = hints
        self.isUSA = isUSA
        self.address = address
        
    def __str__(self):
        retStr = ""
        retStr += "Name: {0}".format(self.name)
        retStr += "; address: {0}".format(self.address)
        retStr += "; can you be shipped anything?: {0}".format(self.shipAnythingRemark)
        retStr += "; gift hints: {0}".format(self.hints)
        
        return retStr

encode=False

def assignSantas(participants):
    assignments = []
    
    #assuming assignments ARE possible
    
    #willShipToUSList =  map(lambda x: x.name, filter(lambda y: y.willShipTo == "US",participants))
    #willShipToIndList =  map(lambda x: x.name, filter(lambda y: y.willShipTo == "India",participants))
    #willShipToBothList =  map(lambda x: x.name, filter(lambda y: y.willShipTo == "Both",participants))
    willShipToRandom = map(lambda x: x.name, filter(lambda y: y.willShipTo != "XXX",participants))
    
    #assign(willShipToUSList,lambda name: lambda x: x.name != name and x.isUSA == "1",assignments)
    #assign(willShipToIndList,lambda name: lambda x: x.name != name and x.isUSA == "0",assignments)
    assign(willShipToRandom,lambda name: lambda x: x.name != name,assignments)
    
    return assignments
    
    
def assign(shippers,filterLambda,assignments):
    for name in shippers:
        filterList = filter(filterLambda(name),participants)
        randInt = random.randint(0,len(filterList)-1)
        santaFor = filterList[randInt]
        participants.remove(santaFor)
        assignments.append((name,santaFor))
        
        
def getParticipants():
    nameIndex = 0
    willShipToIndex = 1
    addressIndex = 2
    shipAnythingRemarkIndex = 3
    hintsIndex = 4
    isUSAIndex = 5
    
    participants = []
    with open('participants2.csv') as csvfile:
        reader = csv.reader(csvfile)
        
        for row in reader:
            participant = Participant(row[nameIndex],row[willShipToIndex],row[addressIndex],row[shipAnythingRemarkIndex],row[hintsIndex])
            participants.append(participant)
            
    return participants

def writeAssignments(assignments):
    with open('assignments.txt', 'w+') as outputFile:
        for assignment in assignments:
            print assignment[0], assignment[1], "\n"
            encString = b64.b64encode(assignment[1].__str__()) if encode else assignment[1].__str__()
            outputFile.write('{0} : {1}\n'.format(assignment[0],encString))
        

if __name__ == "__main__":
    participants = getParticipants()
    assignments = assignSantas(participants)
    writeAssignments(assignments)