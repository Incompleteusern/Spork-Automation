import random
string = "christian never says fredh anymore"
strlst = [x * random.randrange(1, 5) if x not in "!/ .,;;\'" else x for x in string]
outstr = "".join(strlst)
print(outstr)

