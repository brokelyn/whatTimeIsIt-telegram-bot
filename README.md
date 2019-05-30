# What Time Is It - 1337

It is a game played in a messanger service of you choice in a group.
The goal is to write `1337` at the time 13:37. If you do so, you get one point.
The member with the most points at the end of the year wins the game.

It is legal to post any other time to the group. If you post the wrong time per example `1337` at 13:38
you get kicked out of the group until the next day.

# Messenger Bot

## Counting

Because counting the scores is a boring task a bot should do this. Sadly WhatsApp does not support
a good API in this project the Telegram API is used to implement the bot.

## Implementation

### Structure

The structure is orientated on a MVC structured because the requirements are almost the same.
We have user which are requesting with chat messages and the bot needs to analyse, compute and return a result
according to those messages.

### Database

We use the database SQLite and the ORM peewee because both are lightweight and easy to understand.
.....


## Getting started

...


## Different Messenger

Due to an interface for a messenger api we cann support different messenger.
You only need to supply a implementation of your messenger using our interface.

### Telegram 

The default messenger will be Telegram because it provides an easy API and a lot possibilities like polls and reply
function.