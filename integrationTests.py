import os


def startTests():
    os.system('behave .\Acceptance\BookStore\ --no-capture --no-capture-stderr')


startTests()
