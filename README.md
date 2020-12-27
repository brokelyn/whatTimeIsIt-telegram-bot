# What Time Is It - 1337

It is a game played in a messanger service of you choice in a group.
The goal is to write `1337` at the time 13:37. If you do so, you get one point.
The member with the most points at the end of the year wins the game.

It is legal to post any other time to the group. If you post the wrong time as example `1337` at 13:38
you will receive a punishment until the next day. This punishment can be a group ban or 
limited rights to interact with the group.

# Messenger Bot

## Counting

Because counting the scores is a boring task a bot should do this. The bot can count score for 
multiple groups and users at once. Users can be in multiple groups as well.

## Implementation

### Structure

The structure is orientated on a MVC structured because the requirements are almost the same.
We have user which are requesting with chat messages and the bot needs to analyse, compute and return a result
according to those messages and messages from the past.

### Database

We use the database SQLite and the ORM peewee because both are lightweight and easy to understand.
This database is used to persist all incoming *Text Messages* and later
save the scores for the different times. 

### Updates

The bot is currently under development. Every important game feature is implemented, but there is
still stuff to improve. To see features of upcoming updates take a look in the issue section of Github.
## Getting started

This application uses some external libraries which can be found in the `requirements.txt` file.
First step is to install the `requirements.txt` with pip. The basic command is `pip3 install -r requirements.txt`
After pip finishes his work you need to 
set some environment variables.

1. Your bot api key should be named: `BOT_API_KEY=`
2. A database url if you use an external db: `DATABASE_URL=`
   Do not set this variable when working in dev mode. If this variable is not set the program will create a local SQLite 
   database in the src directory.

Then you should be able to start the application by calling `python3 main.py`
in the `src` folder of the project.

### peewee

As ORM we use `peewee`. To get more information take a look here

[Link to peewee docs page](http://docs.peewee-orm.com/en/latest/)

### telegram-bot

A Github repo is used to manage the telegram-bot-api. This repo is called `python-telegram-bot`.

To get more information take a look here

[Link to github telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

## Telegram

### Why Telegram

Telegram has a lot great features and one of the best is the API which allows
developer to create their own bots for different kinds of usage.

### Python-Telegram-Bot

In this project we are using a framework from github which implements
the telegram api. Thanks for this awesome framework!
Link to them https://github.com/python-telegram-bot/python-telegram-bot
