# TeamFightChaticts

## About
This repository contains tools to enable Twitch stream viewers to remote-control a TFT game client.

## Quickstart
For a quickstart, run the following steps:

**1) Install Prerequisites**

- Install Python3 - https://www.python.org/downloads/
- Install Tesseract - https://tesseract-ocr.github.io/tessdoc/Home.html#binaries

**2) Download Source Code**

```sh
git clone https://github.com/Jarr0d161/TeamFightChaticts
cd TeamFightChaticts
```

**3) Configure App Settings**

Open the app_settings.json file with a text editor of choice.

```sh
# Linux
gedit config/app_settings.json
```

```sh
# Windows
notepad config\app_settings.json
```

Fill in the following attributes:

```txt
tesseract_rootdir: Tesseract installation root directory
twitch_connection
  chatbot_name: Twitch chatbot name
  password: Twitch authentication token
```

**4) Install Pip Dependencies**

```sh
python3 -m pip install -r requirements.txt
```

**5) Run the App**

```sh
python3 -m teamfightchaticts
```

## Supported Chat Commands
Following table shows all commands supported:

| Command           | Description                    | Example           |
| ----------------- | ------------------------------ | ----------------- |
| shop(1-5)         | Buy unit in shop               | shop1             |
| [field1][field2]  | Place / switch unit            | w1r5              |
| sellw(1-9)        | Sell unit (from bench)         |                   |
| roll / reroll     | Reroll shop                    |                   |
| lvl / lvlup       | Level up                       |                   |
| collect           | Collect items with avatar      |                   |
| row(1-8)          | Walk row with avatar           | row4              |
| aug(1-3)          | Select augment                 | aug2              |
| (itemslot)(field) | Run (upwards) in item carousel | bw3               |
| lock / unlock     | Lock / unlock store            |                   |


## License
This project is available under the Apache 2.0 License's terms.
