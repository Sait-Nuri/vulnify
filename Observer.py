from __future__ import annotations
from abc import ABC, abstractmethod
import sys
import Utils


class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    # default constructor 
    def __init__(self, vendorname): 
        self.VENDOR = vendorname

    def update(self, subject: Subject) -> None:
        """
        Receive update from subject.
        """

        print("-- " + self.VENDOR + " Observer --")
        
        # This check should be done first before anything in this method
        self.checkMessenger()
        self.messenger.compose(subject._package)
        self.messenger.send()

    
    def addMessenger(self, msgrname) -> None:
        """
        Add a notification channel to inform user
        """
        self.messenger = Utils.newMessenger(msgrname)

        if self.messenger:
            print("[+] New messenger added")

    def checkMessenger(self):
        """
        Check if any messenger is set
        """
        if not self.messenger:
            print("[-] No messenger assigned for " + self.VENDOR)
            print("[!] Exiting...")
            sys.exit()

"""
Concrete Observers react to the updates issued by the Subject they had been
attached to.
"""

class Microsoft(Observer):
    # default constructor 
    def __init__(self): 
        super(Microsoft, self).__init__("Microsoft")


    def update(self, subject: Subject) -> None:

        print("-- " + self.VENDOR + " Observer --")
        # This check should be done first before anything in this method
        self.checkMessenger()
            
        data_list = []
        vendor_name = ""
        for entry in subject._package:
            
            try:
                vendor_name = str(entry.get('software').get('vendor'))
                if vendor_name == "microsoft": data_list.append(entry) 
            except AttributeError:
                pass
        
        if data_list:
            self.messenger.compose(data_list)
            self.messenger.send()


class General(Observer):

    # default constructor 
    def __init__(self): 
        super(General, self).__init__("General")

    # No need for specification, call parent update
    def update(self, subject: Subject) -> None:
        super(General, self).update(subject)
