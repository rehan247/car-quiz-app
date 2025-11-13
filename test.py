message = input("write a message: ")
print("please type a cipher 1-25")
for i in range(0,len(message)):
    temp = ord(message[i])
    temp = temp+5 
    if (temp>122):
        temp=temp-26
    print (chr(temp))

