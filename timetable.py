from settings import Settings
from urllib.request import urlopen
from lecture import Lecture
import os.path
import datetime

class TimeTable:
    
    def __init__(self, settings:Settings):
        self.settings = settings
        self.lectures = []
        
        #Checks to see if there is an already existant directory
        if(settings.ics_online == "NULL"):
            print("No calander link found, please login to: https://studentrecord.aber.ac.uk/en/timetable.php")
            print("Copy 'Timetable iCal feed link', then paste link below.")
            #Ask for link until valid one given
            while(True):
                url = input("link: ")
                if(self.download(url)):
                    break;
                else:
                    print("The link provided is invalid, link should be similar to: https://studentrecord.aber.ac.uk/en/ical.php?user=xxxxxxxxxxxxxxxx")
                    
        if not self.updateLocal():
            self.readLocal()
         
            
    def updateLocal(self)->bool:
        now = datetime.datetime.now()
        last_update = datetime.datetime.strptime(self.settings.ics_fetched, '%Y/%m/%d')
        
        age_d = now-last_update
        age = age_d.days
        print("Local calender age: {:d} days".format(age))
        if(age >= int(self.settings.update_freq)):
            self.download(self.settings.ics_online)
            return True
        else:
            return False

         
    def download(self, onlineLink) -> bool:
        Lecture.records_loaded = 0;
        print("Downloading calender, please wait")
        
        #Download the file and read the data into a local file while
        #parsing the data.
        fp = open(self.settings.ics_local + "_temp", "w+")
        
        try:
            data = urlopen(onlineLink)
            record = {}
            records = []
             
            for line in data:
                line = line.decode()
                line = line.rstrip()
                fp.write(line + "\n");
                if("BEGIN:VEVENT"  == line[0:12]):
                    record = {}
                if("DTSTART:" == line[0:8]):
                    record["START"] = line[8:]
                if("LOCATION:" == line[0:9]):
                    record["LOCATION"] = line[9:]
                if("DESCRIPTION:" == line[0:12]):
                    record["DESC"] = line[12:]
                if("SUMMARY:" == line[0:8]):
                    record["SUMMARY"] = line[8:]
                if("DTEND:" == line[0:6]):
                    record["END"] = line[6:]
                if("END:VEVENT" == line[0:10]):
                    records.append(Lecture(record, self.settings))
                    
            #End of the loop, close the file being written
            fp.close()
            print("Download complete, {:d} lectures found".format(Lecture.records_loaded))
        except:
            #An error occured, close the file and return false
            print("Something went wrong, please check that you are online and"
                  + " the provided link is correct")
            fp.close()
            return False
        
        #All went well, check there were lecutres read in and if so update settings
        if(Lecture.records_loaded > 0):
            now = datetime.datetime.now()
            self.lectures = records
            self.settings.ics_online = onlineLink
            self.settings.ics_fetched = str("{:d}/{:d}/{:d}".format(now.year, now.month, now.day))
            self.settings.create()
            
            #remove the old file and add the new one
            if(os.path.exists(self.settings.ics_local)):
                os.remove(self.settings.ics_local)
            os.rename(self.settings.ics_local + "_temp", self.settings.ics_local)
            return True
        else:
            print("Something went wrong, please check that you are online and"
                  + " the provided link is correct")
            return False
        
        
    def readLocal(self) -> bool:
        fp = open(self.settings.ics_local)
        record = {}
        records = []
        
        for line in fp:
            line = line.rstrip()
            if("BEGIN:VEVENT"  == line[0:12]):
                record = {}
            if("DTSTART:" == line[0:8]):
                record["START"] = line[8:]
            if("LOCATION:" == line[0:9]):
                record["LOCATION"] = line[9:]
            if("DESCRIPTION:" == line[0:12]):
                record["DESC"] = line[12:]
            if("SUMMARY:" == line[0:8]):
                record["SUMMARY"] = line[8:]
            if("DTEND:" == line[0:6]):
                record["END"] = line[6:]
            if("END:VEVENT" == line[0:10]):
                records.append(Lecture(record, self.settings))
        
        self.lectures = records
        
    def printNextLecture(self):
        next_lecture = None
        next_delay = 31557600
        now = datetime.datetime.now()
        
        for l in self.lectures:
            start_time = l.getDateTime()
            diff = (start_time - now).total_seconds()
            if(diff > 0):
                if(diff < next_delay):
                    next_delay = diff;
                    next_lecture = l
        next_lecture.printLecture()

    def printDayLectures(self):
        now = datetime.datetime.now()
        for l in self.lectures:
            lecture = l.getDateTime()
            if(lecture.day == now.day):
                if(lecture.month == now.month):
                    if(lecture.year == now.year):
                        l.printLecture()
    
    
            
                                        
      
            
            
            
        
