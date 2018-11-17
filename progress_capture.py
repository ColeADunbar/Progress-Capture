# Progress_Capture
from tkinter import *
import time




"""
the goal is to write a program that opens in a new window and sets a timer to
go off every X=40 minutes and asks you to log what you have accomplished in those
X mins

"""

another=True
duration=0
WIDTH=25
goallist=[]

def listclean(l):
    return [x for x in l if x.strip()]

#load goallist
with open("goallist.txt","r") as goallisthandle:
    goallist=goallisthandle.readlines()
    goallist=listclean(goallist)

if True:
    #review/get new goals
    print("enter goals seperated by 'return':\n")
    x=input("".join(goallist))
    while x.strip()!="":
        goallist.append(x)
        x=input()
    #set timer
    y=input("pick timer duration, default {} mins:\t".format(duration))
    try:
        float(y)
        duration=int(y)
    except ValueError:
        print("that doesn't look like a number, moving on with duration={} mins".format(duration))
    print("\n~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~.~\n")

while another==True:
    #make a timer
    print("sleeping for {} minutes...".format(duration))
    for i in range(duration):
        time.sleep(60)
    print("done sleeping!\n")

    #make a new window
    root=Tk();
    root.geometry('{}x{}+{}+{}'.format(800,400,100,100))
    root.title("Progress_Capture")

    #duration clicker
    dur=Entry(root, width=2, highlightbackground="yellow")
    dur.grid(column=0,row=0)
    dur.insert(END, duration)

     #past goals title
    pastgoal=Label(root, text="Past Goals")
    pastgoal.grid(column=1,row=1)
    #future goals title
    goal=Label(root, text="New Goals")
    goal.grid(column=2,row=1)
    # lets populate our goals
    listrow=2
    state=[]
    pastgoaltext=[]
    newgoaltext=[]
    for i, text in enumerate(goallist) :
        #checkboxe
        s=IntVar()
        chk=Checkbutton(root, var=s)
        state.append(s)
        chk.grid(column=0,row=listrow+i)

        #past goals
        pastgoaltext.append(Entry(root, width=WIDTH))
        pastgoaltext[i].insert(END, text.rstrip())
        pastgoaltext[i].grid(column=1,row=listrow+i)

    #future goals
    nextrow=2
    for i in range(3):
        newgoaltext.append(Entry(root,width=WIDTH))
        newgoaltext[i].grid(column=2,row=nextrow)
        nextrow+=1

    newgoaltext[0].focus()

    def newgoalbox():
        global newgoaltext
        global nextrow
        newgoaltext.append(Entry(root,width=WIDTH))
        newgoaltext[nextrow-2].grid(column=2,row=nextrow)
        newbox.grid(column=2,row=nextrow+1)
        nextrow+=1
    newbox=Button(root, text="+", highlightbackground="blue", command=newgoalbox)
    newbox.grid(column=2, row=nextrow)

    #write to goallist
    def save_work():
        global goallist
        global duration
        #update duration
        duration=int(dur.get())
       #remove accomplished goals from goallist and update edited goals
        remove=[d.get() for d in state]
        goallist=[]
        for i in range(len(pastgoaltext)):
            goallist.append(pastgoaltext[i].get()+"\n")
        goallist=[d for (d, r) in zip(goallist, remove) if not r]

        #add new goals to goallist
        for i in range(len(newgoaltext)):
            if newgoaltext[i].get()!="":
                goallist.append(newgoaltext[i].get()+"\n")

    #stop button
    def stop_work(*arg):
        global another
        another=False
        #save and quit
        save_work()
        root.destroy()

    stop=Button(root, text="Stop working", highlightbackground="red", command=stop_work)
    stop.grid(column=1,row=0)

    #restart timer button
    def continue_work(*arg):
        save_work()
        root.destroy()

    again=Button(root, text="Keep working", highlightbackground="green", command=continue_work)
    again.grid(column=2,row=0)
    #hit return to continue
    root.bind('<Return>', continue_work)
    #hit esc to exit
    root.bind('<Escape>', stop_work)
    #keep window open
    root.mainloop()



#write goallist to file
with open("goallist.txt","w") as goallisthandle:
    goallisthandle.truncate(0)
    for i in listclean(goallist):
        goallisthandle.write(i)

print("Okay, good work today")
print("Goals you still have:\n")
print(*goallist, sep="")

