#!/usr/bin/env python3


from urllib.request import urlopen
from settings import Settings
from timetable import TimeTable
import sys


settings = Settings()
timetable = TimeTable(settings)




def menu():
    print("")
    print("-----------------Menu-----------------")
    print("1: Show next lecture")
    print("2: Show day lectures")
    print("3: Check for calender update")
    print("4: Close program")
    i = int(input("Selection: "))
    
    if(i == 1):
        timetable.printNextLecture()
    if(i == 2):
        timetable.printDayLectures()
    if(i == 3):
        timetable.download(settings.ics_online)
    if(i == 4):
        sys.exit()
        
    #All loaded, run main menu
while(True):
    menu()
