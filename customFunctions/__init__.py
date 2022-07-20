
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
        try:
            useAmount = float(var.pop(0))    # second element is the amount, integer
        except Exception as e:
            useAmount = 0
        useType = str(var.pop(0))      # third element is the type, string
        useDesc = str(' '.join(var))   # the rest is the desc, string
        return useAmount, useType, useDesc
    except Exception as e:
        print(e)

def saveToFile(var):
    import os
    import pandas
    try:
        # this section saves to a file based on the format:
        # year-month-userID
        # inside, the format will be
        # year, month, day, hour, minute, cost, type, desc

        # this function accepts a dictionary of format
        #dict = {
        #    'cost': 'asdf',
        #    'type': 'asdf',
        #    'desc': 'asdf',
        #    'year': 'asdf',
        #    'month': 'asdf',
        #    'day': 'day i guess',
        #    'hour': 'asdf',
        #    'minute': 'asdf',
        #    'user': 'asdf'
        #}
        targetDir = os.path.normpath(os.path.join(os.getcwd(), 'data'))
        filename = str(var['year']) + "_" + str(var['month']) + "_" + str(var['user']) + '.csv'
        # removing illegal characters from filename
        for i in ['<', '>', '@']:
            filename = filename.replace(i, "")
        filename = os.path.normpath(os.path.join(targetDir, filename))

        # checking for target directory, making it if it does not exist
        if not os.path.isdir(targetDir):
            # if false then create directory
            os.makedirs(targetDir)

        # this section will do the saving
        toSave = [var['year'], var['month'], var['day'], var['cost'], var['type'], var['desc']]
        toSave = pandas.DataFrame(toSave).transpose()
        # saving this to the csv file
        toSave.to_csv(filename, mode='a', header=False, index=False)

        print('saved to' + str(filename))
        return True
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