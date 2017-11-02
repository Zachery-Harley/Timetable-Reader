import datetime



class Lecture:
    records_loaded = 0
    
    def __init__(self, record, settings):
        Lecture.records_loaded += 1 
        self.settings = settings
        #Store the details for the lecturer
        self.start = Lecture.getDate(record["START"])
        self.end = Lecture.getDate(record["END"])       
        self.summary = record["SUMMARY"]
        self.desc = record["DESC"]
        self.location = record["LOCATION"]
        
        #Check and account for day light savings
        if(self.isDST()):
            self.start["HOUR"] += 1;
            self.end["HOUR"] += 1;
        
        self.getDuration()
        

        
    def getDuration(self):
        dateStart = self.start
        dateEnd = self.end
        h = dateEnd['HOUR'] - dateStart['HOUR']
        m = dateEnd['MIN'] - dateStart['MIN']
        self.dHours = h
        self.dMins = m
        
    @staticmethod    
    def getDate(time):
        dateTime = {}
        dateTime['YEAR'] = int(time[0:4])
        dateTime['MONTH'] = int(time[4:6])
        dateTime['DAY'] = int(time[6:8])
        dateTime['HOUR'] = int(time[9:11])
        dateTime['MIN'] = int(time[11:13])
        return dateTime
     
    def isDST(self):
        target_date = datetime.datetime(self.start["YEAR"],
                                        self.start["MONTH"],
                                        self.start["DAY"]
                                        , 0 , 0 , 0)
        dst = self.settings.time_zone.localize(target_date, is_dst=None)
        
        if bool(dst.dst()) is True:
            return True
        else:
            return False
            
    def getDateTime(self):
         start_time = datetime.datetime(self.start["YEAR"],
                                        self.start["MONTH"],
                                        self.start["DAY"],
                                        self.start["HOUR"] , self.start["MIN"] , 0)
         return start_time
    
    def printLecture(self):
        print("")
        s = self.start
        print("----------------Date: {:d}/{:d}  Time: {:d}:{:d}-------------------".format(
                              s['DAY'], s['MONTH'], s['HOUR'], s['MIN']))
        print(self.summary)
        print("Location: " + self.location)
        print("Duration: {:d} hours, {:d} minuets".format(self.dHours, self.dMins))
        
