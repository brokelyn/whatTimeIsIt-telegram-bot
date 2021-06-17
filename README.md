# What Time Is It - 1337

It is a game played in a messenger service of your choice in a group.
The goal is to write `1337` at the time 13:37. If you do so, you get one point.
The member with the most points at the end of the year wins the game.

It is legal to post any other time to the group. If you post the wrong time as
example `1337` at 13:38 o'clock you will receive a punishment until the
next day. This punishment can be a group ban or limited rights to
interact with the group.

# Messenger Bot

## Counting

Because counting the scores is a boring task a bot should do this.
The bot can count score for multiple groups and users at once. Users
can be in multiple groups as well.

## Usage

When creating a new bot it is important to disable `Privacy mode`. Otherwise
the bot will not be able to read all messages in the chat and therefore
cannot count the scores. It can be disabled by the `BotFather`.

### Commands

There are a few different commands to use and control the bot. Most of the
commands can only be used inside a group. If the command is not available in
a private chat, the bot will notify you.

#### Settings

Use the `/settings` command to get an overview over settings for the group.

1. `Violation Action` this will be the action when a user posts a wrong time
  1. `ban` the user will be removed from the group and can join by an invite link
  2. `permission` the user will not be able to interact with the group except of reading messages
  3. `none` no punishment for the user, but wrong times will be mentioned by the bot
2. `Timezone` by clicking on that button the timezone of the group can be changed
3. `Auto Events` when a user posts a time the according statistic will be printed one minute later
4. `Show Invite Link` this will display the current group invite link

#### Events

Events can be used to display statistics to a specific time. The
statistic will be posted one minute after the time and repeated daily.
Events can be active while `Auto Events` is enabled.
There are a few commands to handle those events:

- `/add_event <4 numbers>` the command will a an event to the time given as parameter
- `/remove_event` will display a inline keyboard where active events can be removed  
- `/events` will list every active event

#### Other

There are a few other commands provided by the bot:

- `/time` when replying to a message this command will return the timestamp of the message
- `/stats <4 numbers>` display the statistic to the time given as parameter
- `/help` displays a help message to explain the commands

### Groups

To use the bot just add it to a group. The bot will then start counting times.
In order for the bot to be able to perform advanced tasks (like banning a
member or creating an invite link) you should give him admin rights.

### Private Chat

The bots actions in private chats are limited. Most of the command are only
available for groups. The bot will tell if any command is not available for
a private chat.

## Getting started

This application uses some external libraries which can be found in the
`requirements.txt` file. First step is to install the `requirements.txt`
with pip. The basic command is `pip3 install -r requirements.txt` After
pip finishes his work you need to set some environment variables.

1. Your bot api key should be named: `BOT_API_KEY=`
2. A SQLite file reference with an absolute path : `SQLITE_FILE=`
3. Or a database url if you use an external db: `DATABASE_URL=`

When developing the usage of an SQLite database is recommended

Then you should be able to start the application by calling `python3 main.py`
in the `src` folder of the project.

## Deployment

This project is lightweight and therefore it runs on an `Raspberry Pi Zero`
in combination with an SQLite database without any problems.
But it can be deployed on every hosting service as well.

### peewee

As ORM we use `peewee`. To get more information take a look here

[Link to peewee docs page](http://docs.peewee-orm.com/en/latest/)

### telegram-bot

A Github repo is used to manage the telegram-bot-api. This repo is
called `python-telegram-bot`.

To get more information take a look here

[Link to github telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

## Telegram

### Why Telegram

Telegram has a lot great features and one of the best is the API which allows
developer to create their own bots for different kinds of usage.

### Python-Telegram-Bot

We are using a project from Github which implements
the Telegram API for python. Thanks for this awesome project!
Link to them https://github.com/python-telegram-bot/python-telegram-bot

## Implementation

### Structure

The structure is orientated on a MVC structured because the requirements
are almost the same. We have user which are requesting with chat messages
and the bot needs to analyse, compute and return a result
according to those messages and messages from the past.

### Database

The project uses an SQLite database and peewee as ORM because both are
lightweight and easy to understand. However it is possible to use an external
database aswell. See `Getting started` section for more details.

### Updates

The bot is currently under development. Every important game feature is
implemented, but there is still stuff to improve. To see features of
upcoming updates take a look in the issue section of Github.
