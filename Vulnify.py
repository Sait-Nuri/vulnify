from __future__ import annotations
from datetime import datetime
from abc import ABC, abstractmethod
from Observer import *
import Utils
import os, sys, json
import requests

class Subject(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from the subject.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
        pass


class DailyCVE(Subject):
    """
    The Subject owns some important state and notifies observers when the state
    changes.
    """

    _observers = []
    """
    List of subscribers. In real life, the list of subscribers can be stored
    more comprehensively (categorized by event type, etc.).
    """

    # default constructor 
    def __init__(self): 
        print("[+] DailyCVE instance created")
        self._package = []
        
        with open(Utils.CONFIG_FILE) as json_file:
            data = json.load(json_file)

        self.LOGFILE_PATH = data['vulndb']['logfiles']
        self.API_ENDPOINT_URL = data['vulndb']['endpoint_url']
        self.API_KEY = data['vulndb']['keys']

        self.today = datetime.today().strftime('%Y%m%d')
        self.file_path = self.LOGFILE_PATH + "/" + self.today
        #self.some_business_logic()
        
    def attach(self, observer: Observer) -> None:
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)


    """
    The subscription management methods.
    """
    def notify(self) -> None:
        """
        Trigger an update in each subscriber.
        """

        print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)

    def run(self) -> None:
        """
        Collects newly created vulnerabilities into a list by comparing previous request's result, then notify them. 
        The vulnerabilities which has been notified previously are saved in a log file
        Each run checks for notified vulns from logfile so that they would be excluded from subsequent API call result. 
        """

        # Checks if logfile exists
        self.__checkLogFileExist()

        # read all content from logfile
        loglist = self.__dumpLogFileToList()
        #print(loglist)
        
        # enable below code block if you need test data
        """
        with open("example.json") as json_file:
            example = json.load(json_file)

        feedlist = example
        """
        
        # API request (comment out if you need test data)
        feedlist = self.__request_api()

        # Compares new results with former entries
        union_list,unique_entries = self.__compareEntries(loglist, feedlist)
        #print("unique entries: " + str(unique_list))

        # Update log file with unique entries received from API call
        self.__updateLogFile(union_list)
        print("[*] Logfile updated")

        # If any unique entry, notify observers
        if(self.__notifyCheck(unique_entries)):
            self._package = unique_entries
            self.notify()

    def __checkLogFileExist(self):
        """
        - if no log file: create empty log file with todays date format
        - call dumpLogToList
        """
        
        print("__checkLogFileExist")

        if os.path.isfile(self.file_path):
            print("[+] log file exist")
        else:
            print("[+] new log file created! " + str(self.file_path))
            os.mknod(self.file_path)
        
    
    def __dumpLogFileToList(self):
        """
        - assumes file already exist.
        - if empty, create empty list
        - if not empty, dump file into list
        """

        print("__dumpLogFileToList")

        filesize = os.path.getsize(self.file_path)

        loglist = []

        if(filesize == 0):
            print("[+] Logfile is empty: " + str(filesize))
        else:
            print("[+] logfile dumped into list")
            loglist = open(self.file_path).read().splitlines()
        
        return loglist
    
    def __request_api(self):
        """
        - insert into list = api_feed
        apikey=[your_personal_api_key]&advisory_date=20180211
        curl -k --data "apikey=aaf8fa1409b1f79964671be4275d55ab&advisory_date=20210115&fields=software_vendor,software_name,software_version" https://vuldb.com/?api

        error checks:
        - check if connection error
        - check if token empty, inform and exit
        - check if not success, inform and exit
        """

        opt = {'apikey': str(self.API_KEY), 
            'advisory_date': self.today,
            'fields': 'software_vendor,software_name,software_version'
        }

        #print(opt)

        r=None
        content=None

        try:
            r = requests.post(self.API_ENDPOINT_URL, data=opt, timeout=10)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Request error", e)
            sys.exit()
        else:
            content = r.json()
            res = content['response']['status']
            if(res == "200"):
                print("[+] API request success..")
                print("[*] Remaining token: " + str(content['response']['remaining']))
                
                if(content['response']['items'] == 0):
                    print("[*] No item received! ")
                    sys.exit()
            else:
                print("[-] API request failed.. Error status: " + str(res))
                sys.exit()
        
        return content

    def __updateLogFile(self, anylist):
        """
        - generic insertion of list
        """

        print("__updateLogFile")
        
        with open(self.file_path, "w") as outfile:
            outfile.write("\n".join(str(item) for item in anylist))
    
    def __compareEntries(self, loglist, feedlist):
        """
        - extract sublist
        - compares entry_ids btw api_feed and loglist
        - merge unique_list + loglist
        - call updatelogfile()
        - extract unique into unique_list even if no unique
        returns a unique datafeed_list if possible
        """
        
        print("__compareEntries()")

        # extract id list
        #print(feedlist)
        entry_list = feedlist["result"]
        entry_id_list = [ entry["entry"]["id"] for entry in entry_list ]

        # extract unique ids
        unique_list = list(set(entry_id_list) - set(loglist))
        #print("unique list: " + str(unique_list))

        # union of unique ids and loglist, then write to logfile
        new_loglist = list(set(entry_id_list) | set(loglist)) 
        #print("merged list: " + str(new_loglist))

        # create unique list by unique ids
        unique_entries = [ entry for entry in entry_list if entry["entry"]["id"] in unique_list ]
        
        return (new_loglist, unique_entries)

    def __notifyCheck(self, unique_list):
        """
        - if unique_list empty, return 0
        - if not empty, call notify()
        """

        print("__notifyCheck")

        if not unique_list:
            print("[+] No unique entry!")
            return False
        else:
            print("[+] unique entry detected.")
            return True
