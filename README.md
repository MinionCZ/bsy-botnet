# BSY BotNet
This project is a part of bonus homework for course of computers security.

## About Project
This project is implementation of botnet in Python. Project consists of two programs, which one serves as slave/bot which runs on infected computer and other one is master which commands all slaves.
Slaves and master are communicating via Dropbox by sending uploading/downloading images with hidden messages.

### Project structure
This project consists of 3 modules: 
- common - serves as library for modules master and slave. Here are some basic common implementations.
- master - this module is implementation of master node in botnet network.
- slave - this module is implementation of slave/bot in botnet network.

## Running project

### Before running
Both slave and master modules have subdirectory called resources.
Here you can find file properties.example.json which contains properties example for slave/master. You must take json inside
these files and copy it into file called properties.json in the same directory. Take a look at parameters there especially you must insert token from your Dropbox account into 
token attribute in json. Take note that properties can be modified to modify behaviour of slaves and master. Properties are loaded only on startup of program.
Last but not least you must install dependencies from requirements.txt via command 'pip install -r requirements.txt'.
### Properties
#### Common properties:
- token - serves as storage for Dropbox token 
- image_generator_mode - this attribute can have these values [random, fractal] which tells the bot if he should use fractal
to generate new images or generate random images. Fractal images can be better to stay subtle, because fractals are quite
aesthetic and some real user might really want to store them on dropbox. On the other side their generation takes time and resources
which might be bad for slave/bot which should be as subtle as possible on infected machine. So there is random mode, which generates random
images which are easy to generate and do not require as many resources as generating fractal. Also names for images are different
based on used mode. In default configuration it is set that bots are using random images and master fractal images.

#### Master's properties
- result_fetch_period - how often will master check uploaded results from bots in seconds
- heartbeat_fetch_period - how often will master check uploaded heartbeats from bots in seconds. Need to be same as heartbeat_post_period attribute in slave's properties.
- copied_files_fetch_interval - how often master checks and downloads copied files from slaves via COPY command in seconds

#### Slave's properties
- heartbeat_post_period - how often slave posts heartbeats in seconds. Must be the same as heartbeat_fetch_period
- command_fetch_period - how often slave downloads new commands from master in seconds

### Running project
Take note that master must be ran first to prepare Dropbox for bots which will connect to it later. Communication is asynchronous so it takes up to 2 * heartbeat_fetch_period
for master to know that bot is dead or new bot is registered. So please be patient. Every time master fetches heartbeats he prints
'List of active bots updated'. List of available bots can be seen always after inserting command to master.

#### Running master
Master can be started from root folder with command:
- python -m master.src.main

Master provides cli interface and can execute one of following commands:
- help - prints you out short description about program and its commands
- exit - exits program. Please be patient, this is only PoC so it takes some time
- w - same as command w in bash
- ls - same as command ls in bash. Can have specified path
- copy - copies specified file from slave. Must have specified path
- exec - executes specified binary
- id - same as id in bash

Take note that parameters and commands are separated via space.
After inserting some command you can choose bot on which do you wish to execute this command. Please insert index specified before uuid.

#### Running slave
Slave can be run with command:
- python -m slave.src.main


