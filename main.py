#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Vulnify
from Observer import Microsoft 
from Observer import General 

def main():
    print("main")

    sub = Vulnify.DailyCVE()

    # For all type of vulnerabilities
    general_observer = General()
    general_observer.addMessenger("Telegram")
    sub.attach(general_observer)

    # For Microsoft only vulnerabilities
    microsoft_observer = Microsoft()
    microsoft_observer.addMessenger("Telegram")
    sub.attach(microsoft_observer)
    
    sub.run()

    return 0

if __name__ == "__main__":
    main()

