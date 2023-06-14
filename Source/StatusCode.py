class StatusCode:
    def __init__(self, startLine=""):
        self.number = -1
        self.message = ""

        if len(startLine) > 0:
            self.parseLine(startLine)

    def __eq__(self, other):
        return self.number == other.number and self.message == other.message

    def parseLine(self, startLine):
        self.number = int(startLine.split(" ")[1])
        self.message = startLine.split(" ")[1] + " " + startLine.split(" ")[2]
