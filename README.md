<h1 align="center">Vulnify</h1>


<h2 align="center">

<img src="https://github.com/Sait-Nuri/vulnify/raw/main/images/logo.png">

</h2>

<p align="center">
  
<img src="https://img.shields.io/badge/-TelegramBot-blue">

<img src="https://img.shields.io/badge/python-%3E%3D3.7.0-blue" >

<img src="https://badges.frapsoft.com/os/v1/open-source.svg?v=103">

</p>


## Description

Vulnify is a vulnerability notification system integrated with **Telegram Bot API** as communication channel, and **VulnDB API** as vulnerability intelligence service. 

This is useful for Cyber Security teams, like cyber threat analysts, to be notified instantly after a new vulnerability revealed.


> This project has scalable code-base in order to integrate more communication services like E-mail, SMS, Voice call or anything else support Python!


## Screenshots

![Link to Image](https://github.com/Sait-Nuri/vulnify/raw/main/images/vulnify.png)

*The bot sends message to the group, in which bot added, when any new vulnerability entry available in Vulndb API.*

## Dependencies

* Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install -r requirements.txt
```

* Only Unix systems supported! (for now)

## Usage


* Create a Telegram Group, [obtain group chat id](https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id#answer-32572159) and save it into **app.config** file
* [Create a Telegram Bot and get token key](https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token), then save it into **app.config** file
* Add that bot into the group
* [Create a Vulndb account](https://vuldb.com/?signup), get the API key and save it into **app.config** file

the final result of **app.config** file below:
```json
{	
"telegram": {"token": "TELEGRAM_BOT_TOKEN_HERE", "group_id": "TELEGRAM_GROUP_CHAT_ID_HERE"},
"vulndb": {"endpoint_url": "hxxtp://...", "keys": "VULNDB_API_KEY_HERE", "logfiles": "/tmp"}
}

```

* Schedule an hourly basis task via crontab or any task scheduler for **main.py** file (*A vps or cloud app service is recommended*)

## Testing

To don't waste Vulndb API request limit (bcz the free API is limited), use **example.json** file for parsing, filtering etc..

In **Vulnify.py** file, comment out API request api method and enable code blocks regarding reading **example.json** file
```python
# feedlist = self.__request_api()

with open("example.json") as json_file:
	example = json.load(json_file)
    
feedlist = example
```

## Roadmap

* **Multiple Vulndb API calls** will be implemented to notify more information about vulnerability, including vulnerability simplicity, exploit availability, vulnerability class etc...
* **Parameterized filtering**, ex: only Windows based vulnerabilities to be notified.
* **More communication channels** will be supported like using Twilio API for SMS, Email, or even Voice Call.

## Contributing
A comprehensive guideline for how to contribute the project in **wiki** page. 

Any contribution to enrich functionality of the project will be considered. 

## License
[MIT](https://choosealicense.com/licenses/mit/)
