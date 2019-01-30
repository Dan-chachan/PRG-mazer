import pygame



def pretty_print(twoDlist):
    for y in twoDlist:
        for x in y:
            if type(x) == str:
                print("!", x, "!", end="")
            else:
                print(x.content, end="")
        print("")
