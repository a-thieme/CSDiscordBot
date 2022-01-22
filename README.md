# CSDiscordBot
### Commands
```
~cs announce : Announces a message to the server
~cs ignore : Blacklists a user from using bot commands
~cs info [optional="course code"] : Retrieves information on the given course, or the current channel if no argument is provided
~cs professor ["Professor name"] : Retrieves information on a specific professor
~cs classes : Retrieves all courses in the COMP major
~cs professors : Retrieves all professors in the COMP department
~cs ping : Pings the bot 
~cs news [optional="course code"] : Retrieves recent ecourseware news on the given course, or the current channel if no argument is provided
~cs test : Tests bot response
~cs shutdown : Softly and safely terminates the bot
```
### To-do list
```
Automate news checking every 2 hours, posting any updates in the correct channel.
Accept news for every section of a course rather than just course 001
Assignment storage that takes user input and stores it for later
Fill out rss information for most sections
Accept math commands
```

### Local Dev

Clone the repo, the run the powershell script `create_env.ps1`

Make sure to have `git` cli installed

Open powershell (preferably in administrator mode)
```cmd
.\create_env.ps1
```