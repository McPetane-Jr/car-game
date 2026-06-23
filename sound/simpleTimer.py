import time
timer = int(input("Enter yo seconds: "))
for i in range(timer,0,-1):
    sec = i%60 #prints remainder
    min = int(i/60)%60
    hrs = int(i/3600)
    print(f"{hrs:02}:{min:02}:{sec:02}")
    #print("Even" if i % 2 == 0 else "Odd")
    time.sleep(1)
