var = ['5', 'food', 'maggi', 'noodals']
print(var)
useAmount = int(var.pop(0))    # second element is the amount, integer
useType = str(var.pop(0))      # third element is the type, string
useDesc = str(' '.join(var))    # the rest is the desc, string

print(useAmount)
print(useDesc)