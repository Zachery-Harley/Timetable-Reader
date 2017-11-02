import configparser
import os.path
import pytz


_settings_file_name = "/home/zah/bin/TTReader/settings.ini"


class Settings:
    local_file_name = "/home/zah/bin/TTReader/local.ics"
    
    
    def __init__(self):
        self.ics_local = "/home/zah/bin/TTReader/local.ics"
        self.ics_online = "NULL"
        self.ics_fetched = "NULL"
        self.update_freq = 7
        self.zone_name = "Europe/London"
        
        #Check if there is a settings file already
        if(os.path.exists(_settings_file_name)):
            print("Loading settings: " + _settings_file_name);
            self.load()
        else:
            print("No settings detected, creating now!")
            self.create()

        self.time_zone = pytz.timezone(self.zone_name)
            
            
    def load(self):
        config = configparser.ConfigParser()
        config.read(_settings_file_name)
        config.sections()
        
        #Read the date in from the settings file
        self.ics_local = config['SETTINGS']['ICSLocal']
        self.ics_fetched = config['SETTINGS']['ICSFetched']
        self.ics_online = config['SETTINGS']['ICSOnline']
        self.update_freq = config['SETTINGS']['UpdateFrequency']
        self.zone_name = config['SETTINGS']['Timezone']
        
    def create(self):
        #Create the file
        fp = open(_settings_file_name, "w+")
        #Write the config to the file
        config = configparser.ConfigParser()
        config['SETTINGS'] = {'ICSOnline': self.ics_online,
                              'ICSLocal': self.ics_local,
                              'ICSFetched': self.ics_fetched,
                              'UpdateFrequency': self.update_freq,
                              'Timezone' : self.zone_name}
        config.write(fp)
        fp.close()
