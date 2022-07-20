
def printTest(var):
    # this is just a testing function, dont mind this
    try:
        print(var)
        return
    except Exception as e:
        print(e)

def parseAmount(var):
    try:
        # converts to string, splits according to space, then removes first element, rejoins
        # and then returns the final thing
        var = str(var)
        var = var.split(" ")
        var.pop(0)                  # removes the first element, which is command
        print(var)
        useAmount = float(var.pop(0))    # second element is the amount, integer
        useType = str(var.pop(0))      # third element is the type, string
        useDesc = str(' '.join(var))   # the rest is the desc, string
        return useAmount, useType, useDesc
    except Exception as e:
        print(e)

def removeCommand(var):
    try:
        # converts to string, splits according to space, then removes first element, rejoins
        # and then returns the final thing
        var = str(var)
        var = var.split(" ")
        var.pop(0)
        var = ' '.join(var)
        return var
    except Exception as e:
        print(e)