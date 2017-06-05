Welcome to pypubg
===================

### Contents

- [pypubg](#gold)
    - [Description](#description)
    - [Installation](#installation)
    - [Example](#example)
    - [Contribute](#contribute)

## Description ##
pypubg is a thin wrapper to call the PUBG tracker API to grab player stats.  pypubg currently only supports python 3.

To use this you will need an api key for pubgtracker.com, you can get one here: https://pubgtracker.com/site-api
Please respect their rate limiting suggestions on their website.

## Installation ##
Simply run

    pip install pypubg

## Example ##

*Getting a PC player's stats*

    From pypubg import players
    players.get_player('akustic', 'your-api-key')

The data is returned to use as a python dictionary.  

## Contribute ##
coming soon
