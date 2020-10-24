import discord
from discord.ext import commands, menus
import dbobj,os
from util_classes import database

# a simple check to gather the users that can use
# webhooks and make sure the author of the command
# is one of those users.
def can_use_webhooks():
  def predicate(ctx):
    user_str = os.environ['WEBHOOKS_USERS']
    user_arr = user_str.split(",")
    return str(ctx.author.id) in user_arr
  return commands.check(predicate)

class webhooks(commands.Cog):
  def __init__(self,bot):
    self.bot = bot

  @can_use_webhooks()
  @commands.command(name="webhook-say",aliases=['ws','s','message'],help="Send a webhook message in this channel if such a webhook exists.")
  async def webhook_test_cmd(self,ctx,*,msg):
    wh = await ctx.channel.webhooks()
    if wh == []:
      await ctx.send("No webhooks in this channel!")
    else:
      profile = database.select_one(dbobj.webhook_profile,user_id=ctx.author.id)
      f = None
      if ctx.message.attachments:
        f = await ctx.message.attachments[0].to_file()
      if profile == [] or profile == None:
        await ctx.message.delete()
        await wh[0].send(msg,file=f)
      else:
        print(profile[1])
        await ctx.message.delete()
        if str(profile[2]) == "None":
          await wh[0].send(msg,username=str(profile[1]),file=f)
        else:
          await wh[0].send(msg,username=str(profile[1]),avatar_url=str(profile[2]),file=f)

  @can_use_webhooks()
  @commands.command(name="webhook-profile",aliases=['wp'],help="Add or update your webhook profile, usable on any webhook accessible by this bot.")
  async def webhook_profile(self,ctx,username,avatar_url=None):
    existing = database.select_one(dbobj.webhook_profile,user_id=ctx.author.id)
    url_string = "None"
    if avatar_url != None:
      url_string = avatar_url
    elif ctx.message.attachments:
      url_string = ctx.message.attachments[0].url
    if existing == [] or existing == None:
      database.insert_row(dbobj.webhook_profile,(ctx.author.id,username,url_string))
    else:
      database.update_data(dbobj.webhook_profile,(username,url_string,ctx.author.id))
    await ctx.send("Profile Updated with username: " + username)
