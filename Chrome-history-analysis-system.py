import os
import sqlite3
import operator
from collections import OrderedDict
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from tkinter import *


def date_to_webkit(dt, tz):
    """Convert local datetime to webkit(utc)"""
    epoch_start = datetime(1601, 1, 1)
    delta = dt - epoch_start - timedelta(hours=tz)
    delta_micro_sec = (delta.days * 60 * 60 * 24 + delta.seconds) * 1000 * 1000
    return delta_micro_sec

def parse(url):
    try:
        parsed_url_components = url.split('//')
        sublevel_split = parsed_url_components[1].split('/', 1)
        domain = sublevel_split[0].replace("www.", "")
        return domain
    except IndexError:
        print("URL format error!")

def analyze(results, picStr):
    for site, count in sites_count_sorted.items():
        print (site, count)

    num = 5 
    plt.bar(range(num), list(results.values())[:num], align='edge')
    plt.xticks(rotation=20)
    plt.xticks(range(num), list(results.keys())[:num])
    plt.title(picStr)
    picName = picStr
    plt.savefig(picName)
    plt.show()
        

##############_______calc_Per__M/H/D/W________
def calcPerMinutes():
    stat3= 30 #how many last minutes we want to calculate
    dt_to = datetime.now()
    dt_from = datetime.now() - timedelta(minutes=stat3)
    tz = 2
    time_to = date_to_webkit(dt_to, tz)
    time_from = date_to_webkit(dt_from, tz)
    select_statement = f"""SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url AND {time_from} < visits.visit_time AND visits.visit_time < {time_to};"""
    
    cursor.execute(select_statement)
    results = cursor.fetchall() #tuple
    sites_count = {} #dict makes iterations easier :D
    sites_count = sitesCountByAllTimeBySlotsTime(results, "Per_Minutes")
    
def calcPerHours():
    stat3 = 4 #how many last hours you want to calculate
    dt_to = datetime.now()
    dt_from = datetime.now() - timedelta(hours=stat3)
    tz = 2
    time_to = date_to_webkit(dt_to, tz)
    time_from = date_to_webkit(dt_from, tz)
    select_statement = f"""SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url AND {time_from} < visits.visit_time AND visits.visit_time < {time_to};"""
    
    cursor.execute(select_statement)
    results = cursor.fetchall() #tuple
    sites_count = {} #dict makes iterations easier :D
    sites_count = sitesCountByAllTimeBySlotsTime(results, "Per_Hours")

def calcPerDays():
    stat3 = 3 #how many last days you want to calculate
    dt_to = datetime.now()
    dt_from = datetime.now() - timedelta(days=stat3)
    tz = 2
    time_to = date_to_webkit(dt_to, tz)
    time_from = date_to_webkit(dt_from, tz)
    select_statement = f"""SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url AND {time_from} < visits.visit_time AND visits.visit_time < {time_to};"""
    
    cursor.execute(select_statement)
    results = cursor.fetchall() #tuple
    sites_count = {} #dict makes iterations easier :D
    sites_count = sitesCountByAllTimeBySlotsTime(results, "Per_Days")
        

def calcPerWeeks():
    stat3 = 4 #how many last weeks you want to calculate
    dt_to = datetime.now()
    dt_from = datetime.now() - timedelta(weeks=stat3)
    tz = 2
    time_to = date_to_webkit(dt_to, tz)
    time_from = date_to_webkit(dt_from, tz)
    select_statement = f"""SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url AND {time_from} < visits.visit_time AND visits.visit_time < {time_to};"""
    
    cursor.execute(select_statement)
    results = cursor.fetchall() #tuple
    sites_count = {} #dict makes iterations easier :D
    sites_count = sitesCountByAllTimeBySlotsTime(results , "Per_Weeks")

# define a function
def showButtons():
    # create four buttons
    button2['state'] = DISABLED
    btn1 = Button(window, text="calculate per minutes", bg="pink", command= lambda: calcPerMinutes())
    btn1.pack(side="left")
    btn2 = Button(window, text="calculate per hours", bg="pink", command= lambda: calcPerHours())
    btn2.pack(side="left")
    btn3 = Button(window, text="calculate per days", bg="pink", command= lambda: calcPerDays())
    btn3.pack(side="left")
    btn4 = Button(window, text="calculate per weeks", bg="pink", command= lambda: calcPerWeeks())
    btn4.pack(side="left")

##############END_______calc_Per__M/H/D/W____________END    
########################################################    

        
def sitesCountByDuration():
    select_statement = "SELECT urls.url, visits.visit_duration FROM urls, visits WHERE urls.id = visits.url AND visits.visit_duration > 0;"
    sites_count = {} #dict makes iterations easier :D
    sites_duration = {} #dict makes iterations easier :D
       
    cursor.execute(select_statement)
    results = cursor.fetchall() #tuple
    
    for url, duration in results:
        url = parse(url)
        if url in sites_count:
            sites_duration[url] += (duration/(1000*60*60))%24 #hours
            sites_count[url] += 1
        else:
            sites_duration[url] = (duration/(1000*60*60))%24
            sites_count[url] = 1  
            
    for url, y in sites_duration.items():
        sites_count[url] = sites_duration[url]/ sites_count[url]
    
    sites_count_sorted = OrderedDict(sorted(sites_count.items(), key=operator.itemgetter(1), reverse=True))
    analyze(sites_count_sorted, "Top-Visited Websites- By Duration")
    
    return sites_count

##############______________________
    
def sitesCountByAllTime(results, strplot):
    select_statement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
    cursor.execute(select_statement)
    results = cursor.fetchall() #tuple
    for url, count in results:
        url = parse(url)
        if url in sites_count:
            sites_count[url] += 1
        else:
            sites_count[url] = 1
    
    sites_count_sorted = OrderedDict(sorted(sites_count.items(), key=operator.itemgetter(1), reverse=True))
    analyze(sites_count_sorted, "Top-Visited Websites-By All Time" + strplot)
    
    return sites_count


def sitesCountByAllTimeBySlotsTime(results, strplot):
    for url, count in results:
        url = parse(url)
        if url in sites_count:
            sites_count[url] += 1
        else:
            sites_count[url] = 1
    
    sites_count_sorted = OrderedDict(sorted(sites_count.items(), key=operator.itemgetter(1), reverse=True))
    analyze(sites_count_sorted, "Top-Visited Websites-By All Time" + strplot)
    
    return sites_count

########################################################    

def sitesCountMorning(results):
    from_time = 8
    until_time = 13
    for url, count, time in results:
        hours=(time/(1000*60*60))%24
        if hours < from_time or hours > until_time:
            continue
        url = parse(url)
        if url in sites_count_morning:
            sites_count_morning[url] += 1
        else:
            sites_count_morning[url] = 1
            
    return sites_count_morning

def sitesCountEvning(results):
    from_time = 17
    until_time = 22
    for url, count, time in results:
        hours=(time/(1000*60*60))%24
        if hours < from_time or hours > until_time:
            continue
        url = parse(url)
        if url in sites_count_evning:
            sites_count_evning[url] += 1
        else:
            sites_count_evning[url] = 1
            
    return sites_count_evning


def sitesCountByMornningNight():
    select_statement = "SELECT urls.url, urls.visit_count, visits.visit_time FROM urls, visits WHERE urls.id = visits.url;"
    cursor.execute(select_statement)
    results = cursor.fetchall() #tuple
    sites_count_morning = sitesCountMorning(results)
    sites_count_evning = sitesCountEvning(results)
    
    sites_count_sorted_morning = OrderedDict(sorted(sites_count_morning.items(), key=operator.itemgetter(1), reverse=True))
    sites_count_sorted_evning = OrderedDict(sorted(sites_count_evning.items(), key=operator.itemgetter(1), reverse=True))
    #analyzeV2(sites_count_sorted_morning,sites_count_sorted_evning)
    num=5
    plt.bar(range(num), list(sites_count_sorted_morning.values())[:num], align='edge')
    plt.xticks(rotation=20)
    plt.xticks(range(num), list(sites_count_sorted_morning.keys())[:num])
    plt.title("Top-Visited Websites - Morning")
    plt.savefig("Top-Visited Websites - Morning")
    plt.show()
    
    
    plt.bar(range(num), list(sites_count_sorted_evning.values())[:num], align='edge')
    plt.xticks(rotation=20)
    plt.xticks(range(num), list(sites_count_sorted_evning.keys())[:num])
    plt.title("Top-Visited Websites - Evening")
    plt.savefig("Top-Visited Websites - Evening")
    plt.show()
    
######################################################## 

class Window():
    def __init__(self):
  
        # Creating the tkinter Window
        self.root = Tk()
        self.root.configure(bg="blue")
        self.root.title("Group Number 3 - Home Page")
        
        self.root.geometry("700x200")
        
        # Create a Label
        label_1 = Label(self.root ,width = 100,text="Close your Chrome engine window !! \n Enter the path to your user's history database (Chrome). Use '\\\\'. \n\n For exmpale: C:\\Users\\iluzh\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
        label_1.pack()

        # Create an entry box
        entry_1 = Entry(self.root)
        entry_1.pack()
        
  
        # Button for closing
        exit_button=Button(self.root, width = 15, text="Submit", command=lambda:self.Close(entry_1))
        exit_button.pack(pady=20)
  
        self.root.mainloop()
  
    # Function for closing window
    def Close(self, entry_1):
        data_path = entry_1.get()
        # Save the input number
        with open('data_path.txt', 'w') as f:
            f.write(data_path)
        # Close the window when done
        self.root.destroy()
  
  
# Running test window
test = Window()



###############################Read path to user's history database (Chrome)#############################################
# Open the txt file to read the user input
f = open("data_path.txt","r")
# Read the user input into a variable
data_path = f.read()
# Print the user input
print("The user input is: " + data_path)
# Close the txt file
f.close()

#---------Create new window------------#
#Create the window
window = Tk()

window.title("Group Number 3") 
window.configure(background='pink') 
window.geometry("1000x500")
window.configure(bg="pink")

#-----------------------------#

#path to user's history database (Chrome)
#data_path = "C:\\Users\\iluzh\\AppData\\Local\\Google\\Chrome\\User Data\\Default" #os.path.expanduser('~')+"/.config/google-chrome/Default/"
files = os.listdir(data_path)
history_db = os.path.join(data_path, 'History')

#querying the db
c = sqlite3.connect(history_db)
cursor = c.cursor() 

sites_count = {} #dict makes iterations easier :D
sites_duration = {} #dict makes iterations easier :D
sites_count_morning = {} 
sites_count_evning = {} 
           
sites_count_sorted = OrderedDict(sorted(sites_count.items(), key=operator.itemgetter(1), reverse=True))


#######################################################################

#Create the Heading
Label(window, text = "Group Number 3", bg = "pink", font = "none 12 bold").pack() 

#Create the Generate My TOP 10 From History Button
button1 = Button(window, text = "Generate My TOP 5 visits From History", width = 70, command =lambda: sitesCountByAllTime(sites_count_sorted, "Top 10")).pack() 

#Create the Generate My TOP 10 Day&Night From History Button
button2 = Button(window, text = "Generate My TOP 5 visitis per slots of time From History", width = 70)#, command =lambda:statementByTime()
button2.pack()
# bind the button to the function
button2.config(command=showButtons)


#Create the Generate My TOP 10 Visit Time From History Button
button3 = Button(window, text = "Generate My TOP 5 average duration of visits From History", width = 70, command =lambda: sitesCountByDuration()  ).pack() 

#Create the Generate My TOP visit in morning and event From History Button
button4 = Button(window, text = "Generate My TOP 5 visits at the Morning&Evning From History", width = 70, command =lambda: sitesCountByMornningNight()  ).pack() 



#Run the main loop
window.mainloop()

