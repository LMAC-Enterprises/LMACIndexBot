The LMAC Index Bot is one of several tools we develop for LMAC. 
It is used to build an index in a database of images donated to the LMAC Image Library.
The short term goal of this software project is to use this index to generate and periodically update an image index post in the Hive network.
In the long term, an online image gallery could also be made using this database as a backend.

# Manual

## 1. How to install

**NOTE: PYTHON3 is required to run this software. The bot can run on Linux, Unix, Windows and Mac.**

Config.py must be modified with the access data of the database that is to be used with the bot.
To do this, simply replace the sample values.

### 1.1 Example

```
class Config:
	# Name of the database. The database and the tables will be generated automatically.
	mysqlDatabaseName = "lildb"
	# Address of the mysql database server.
	mysqlHost = "localhost"
	# Name of the user who has access to the database.
	mysqlUser = "testuser"
	# Password of the user who has access to the database.
	mysqlPassword = "testpassword"
	# The tag the bot has to search for to find the relevant posts. 
	indicatorTag = "lil"
	# Maximum posts the bot is allowed to load per runtime session.
	maximumPostsToLoad = 100

	# True enables the whitelist mode. Only image data of whitelisted authors will then be added to the database.
	whitelistMode = True				
	# This is the username that signs the addding of new whitelisted authors when the initialWhitelist will be saved to the database.
	initialWhitelisterName = "-BOT-"	
	# Initial whitelist. Will be added to the database whenever the database doesn't exist at start.
	initialWhitelist = ["whitelistedhiveuser1", "whitelistedhiveuser2", "whitelistedhiveuser3", "whitelistedhiveuser4"]
```

### 1.2 Cronjob

Create a cronjob and let it start the python file LMACIndexBot.py in the intervals you want it to run.

**Example:**

```
$ crontab -l
$ crontab -e
  30 1 * * * python /PATH TO THE BOT CODE FILES/LMACIndexBot.py
```

### 1.3 Dependencies

This software uses the third party packages described below.

- beem (https://github.com/holgern/beem)

## 2. Editing

The code was written in Visual Studio. You can open the project by loading the file LMACIndexBot.pyproj in VS2015(+).

## 3. Data format

The bot searches Hive posts for indicators that suggest that images should be added to the LIL database.
Even though more are planned, there is only one valid indicator at the moment.  It is the table structure described below. 
The important thing here is the structure of this table. Have a look at the use of classes and columns.

```
<table class="lil">
 
<tr>
<td class="lil-title">EN: It's my dog Frieda.<br/><br/>DE: Es ist mein Hund Frieda.</td>
<td class="lil-tags">dog, pet, monster, cutout</td>
<td class="lil-image"><img src="https://files.peakd.com/file/peakd-hive/quantumg/AJpiqN2PymNJZDWdamEiDovJExYA78MYRFNDvPoswonawwmPBKVBv8YkHTBtmJ2.png" width="300"/></td>
</tr>
<tr>
<td class="lil-title">EN: A shell I once found on the Rhine (river). <br/><br/>DE: Eine Muschel die ich einst am Rhein fand.</td>
<td class="lil-tags">shell, ocean, animal, fish, sea, cutout</td>
<td class="lil-image"><img src="https://files.peakd.com/file/peakd-hive/quantumg/AJmqzZgbEknZ6qPZTZx1mVSo6kiGAtYehyPF587QzmakmyeFEQt6iowLr2W3EvC.png" width="300"/></td>
</tr>
<tr>
<td class="lil-title">EN: My dog Frieda as she rolls around on the floor.<br/><br/>DE: Mein Hund Frieda, wie sie sich auf dem Boden wälzt.</td>
<td class="lil-tags">dog, pet, monster, cutout</td>
<td class="lil-image"><img src="https://files.peakd.com/file/peakd-hive/quantumg/48SM28mkJ9aTpQFZFiJfp9y61btEbYjAjpxtmbPZdsfaksRCvPY8zNWsbvtUxcaqsh.png" width="300"/></td>
</tr>

</table>
```

**Example:**

<table class="lil">
 
<tr>
<td class="lil-title">EN: It's my dog Frieda.<br/><br/>DE: Es ist mein Hund Frieda.</td>
<td class="lil-tags">dog, pet, monster, cutout</td>
<td class="lil-image"><img src="https://files.peakd.com/file/peakd-hive/quantumg/AJpiqN2PymNJZDWdamEiDovJExYA78MYRFNDvPoswonawwmPBKVBv8YkHTBtmJ2.png" width="300"/></td>
</tr>
<tr>
<td class="lil-title">EN: A shell I once found on the Rhine (river). <br/><br/>DE: Eine Muschel die ich einst am Rhein fand.</td>
<td class="lil-tags">shell, ocean, animal, fish, sea, cutout</td>
<td class="lil-image"><img src="https://files.peakd.com/file/peakd-hive/quantumg/AJmqzZgbEknZ6qPZTZx1mVSo6kiGAtYehyPF587QzmakmyeFEQt6iowLr2W3EvC.png" width="300"/></td>
</tr>
<tr>
<td class="lil-title">EN: My dog Frieda as she rolls around on the floor.<br/><br/>DE: Mein Hund Frieda, wie sie sich auf dem Boden wälzt.</td>
<td class="lil-tags">dog, pet, monster, cutout</td>
<td class="lil-image"><img src="https://files.peakd.com/file/peakd-hive/quantumg/48SM28mkJ9aTpQFZFiJfp9y61btEbYjAjpxtmbPZdsfaksRCvPY8zNWsbvtUxcaqsh.png" width="300"/></td>
</tr>

</table>