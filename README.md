# Discord Webhook Bot

Welcome! This repository is for, as you have hopefully already guessed, a webhook bot for Discord. Hosted individually on Heroku (though it can be locally installed), this code just connects to Discord through a bot profile you create using the Discord Developer Portal, and then waits for you to use it. It's really nothing special.

## Setup

Unfortunately, this bot isn't all ready to go from step one. There's more to it, although thankfully not much. This section details in steps how to set up your own instance of this single-server bot.

### 1: Bot Profile

First things first, create a Discord bot profile through the Discord Developer portal [here.](https://discord.com/developers/) Find the bot token and copy it into a text file so it can easily be found later. At this time, designate two channels of your choice in a Discord server you own (or have moderator privileges on) as logging channels. This will allow the bot to log certain events to those channels for reference later, so it's very important.

### 2: Heroku App

Next you need to add this bot to your Heroku account by pressing this button:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/geekkid1/WebhookBot)

First it will probably ask you for an app name, which you can set to anything you want really, and then after that some config variables. This is where the token and channel ids come in. Paste them into their respective config variable boxes. Then continue. This will, if it works correctly, auto-deploy the app to your Heroku account. If you don't have one, this will prompt you to create one or log in to one.

### 3: Configure Database (easy)

Now that the heroku app has been fully set up, all you have to do is turn it on, and then turn it back off. The "ready" event will trigger lines of code that set up the database *for* you. During this step you may also optionally invite it to servers, but only *after* it has turned on for the first time. Now might be a good time to invite it to the server you do logging on. If you don't do it now, you'll have to do it in the next step anyway. The next step also has more details on how to do these things.

### 3b: Configure Database (hard) (DEPRECATED)

**Note:** As of a recent update... this part of the README is deprecated! Inside the bot's `on_ready` event is some code that will create the database tables if they don't already exist. Which means that all this information on how to make the tables manually is completely useless. I'm still leaving it here in case you need to repair anything by hand.

This step is a little bit more hands-on than the previous two, and really just sets up the database so everything can be stored in the right place. After the app has been deployed to your Heroku account, install the Heroku CLI on your computer if you haven't already, as well as the PostgreSQL program itself (get the insaller [here](https://www.postgresql.org/download/), look for solutions on [this page](https://devcenter.heroku.com/articles/heroku-postgresql#pg-psql) and others linked by that page if you can't figure out how to do something). Then run the command `heroku pg:psql -a [app-name]`, replacing `[app-name]` with the name of your app. The first time you run this command it will ask you to log in so it knows you have access to the app.

This will connect your local command prompt to the database the PostgreSQL addon for Heroku set up for you. From here we must create the tables that will store your data. Start with the `servers` table:

```sql
CREATE TABLE IF NOT EXISTS servers (
id bigint PRIMARY KEY,
prefix text);
```

It should give you a confirmation line in the command prompt, and now you can move on to the `webhook_profile` table:

```sql
CREATE TABLE IF NOT EXISTS webhook_profile (
user_id bigint PRIMARY KEY,
username text,
avatar_url text);
```

This rounds out all of the table creation needed, and you can either quit the process on the command line or just quit the entire command line program for now.

### 4: Final Checks

This is the final step before you can start using the bot, and it kinda consists of multiple actions. Not to fear though, they are relatively simple and you'll be getting the bot up and running in no time at all.

First things first, you actually have to turn on the bot. Go in to the Resources tab on your Heroku application's dashboard. There should be a single Dyno listed under "free dynos" labeled "worker". Click on the button with the pencil on it, click the toggle switch so that it's on, then click "confirm". This will start the bot process.

Now that you've turned it on, go back to the Discord Developer Portal, generate an invite link for your bot, and invite it to the server(s) you intend to use it on. Additionally if the logging channels are on a different server make sure it's also there, or it won't be able to log errors. (you may have already invited it to some of these servers in step 3)

After that, you're done! If you have any additional issues, please ask me. I'm looking in to finding a way to get automatic updates and will let you know if I do. There's probably some Heroku resource somewhere that I just haven't found yet.
