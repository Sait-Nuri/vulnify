from __future__ import annotations
from abc import ABC, abstractmethod
import sys, json
import requests
import telegram

    # Helper method to create messenger object
def newMessenger(msgrname):
    if(msgrname == "Telegram"):
        return Telegram.getInstance()
    elif(msgrname == "Twilio"):
        print("[-] Twilio API not implemented")
        pass #return Twilio()
    else:
        print("[-] " + msgrname+ " object not found!")
        return None

CONFIG_FILE = "api.config"

class Messenger(ABC):
    """
    Messaging interface for different platforms
    Example: SMS, Email, Voice Call etc..
    """

    @abstractmethod
    def compose(self, data_list):
        pass
    
    @abstractmethod
    def send(self):
        pass

class Telegram(Messenger):
    __instance = None
    
    @staticmethod 
    def getInstance():
        """ Static access method. """
      
        if Telegram.__instance == None:
            Telegram()
    
        return Telegram.__instance
    
    def __init__(self):
        """ Virtually private constructor. """
    
        if Telegram.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Telegram.__instance = self
            print("[+] Telegram instance created")
            
            with open(CONFIG_FILE) as json_file:
                data = json.load(json_file)

            self.AUTH_TOKEN = data['telegram']['token']
            self.GROUP_ID = data['telegram']['group_id']
            
    def compose(self, data_list):
        self.text = ""
        
        for entry in data_list:
            try:
                self.text += "<b>ID</b>: " + entry.get('source').get('cve').get('id') + "\n"
            except AttributeError:
                self.text += "<b>ID</b>: None\n"
            
            software = ""
            vendor = ""
            try:
                vendor = str(entry.get('software').get('vendor'))
                software = str(entry.get('software').get('name'))
            except AttributeError:
                pass

            self.text += "<b>Product</b>: " + vendor + " " + software + "\n"
            #print("Product: " + product)
            
            self.text += "<b>Title</b>: " + entry['entry']['title'] + "\n"
            self.text += "<b>Risk</b>: " + entry['vulnerability']['risk']['name'] + "\n\n"
        
        print(self.text)
        #self.text = "**test** *message* for telegram group test"
    
    def send(self):
        bot = telegram.Bot(self.AUTH_TOKEN)
        
        try:
            bot.send_message(int(self.GROUP_ID), self.text, parse_mode='HTML')
        except telegram.TelegramError as e:
            print(e)

class Twilio(Messenger):
    pass

class CVEmailer(Messenger):
    """
    Send CVE notifications via email
    """
    def __init__(self):
        print("[+] CVEmailer instance created. ")

    def compose(self, data_list):

        # parse cve data here, store in content variable
        self.content = info_data
        print("compose()")
    
    def send(self):
        API_AUTH = self.config['auth']
        API_ENDPOINT_URL = self.config['endpoint']

        headers = {
            'Authorization': str(API_AUTH),
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        data = {
            'from': "",
            'to': "",
            'subject': "",
            'text': self.content
            #'html': "<h1>Html body</h1><p>Rich HTML message body.</p>"
        }

        #print(opt)

        r=None
        try:
            r = requests.post(API_ENDPOINT_URL, data=data, headers=headers, timeout=10)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Request error", e)
            return False
        else:
            content = r.json()
            if(res == "200"):
                print("[+] API request success..")
                return True
            else:
                res = content['requestError']['serviceException']['messageId']
                print("[-] API request failed.. Error message: " + str(res))
                return False