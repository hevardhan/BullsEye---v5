sent = 0
ack = 0 

num = int(input("Enter the Window Size :"))

while True:

    for x in range(num) :
        
        sent +=1
        print(f"Frame {sent} Sent")
        
        if sent == num:
            break
    
    gg = int(input("Enter ACK"))
    
    if gg == num:
        break
    else:
        sent = gg