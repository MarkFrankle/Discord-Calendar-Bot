from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import calendar
import datetime
import discord
from discord.ext import commands
import math
from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *


# discord.py calls groups of commands cogs
# cogs can also be handlers for different types of events
# and respond to changes in data as they happen

# setup
class CalendarCog:
    def __init__(self, bot):
        self.bot = bot

    # get the calendar
    @commands.command()
    async def getCalendar(self, ctx):
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        await ctx.send('Getting the upcoming 10 events')
        store = file.Storage('credentials.json')
        creds = store.get()
        service = build('calendar', 'v3', http=creds.authorize(Http()))
        events_result = service.events().list(calendarId='uw.edu_1g1n97mk4kumu34fooleqqkbn8@group.calendar.google.com', timeMin=now,
        # events_result = service.events().list(calendarId=*, timeMin=now,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            await ctx.send('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            # await ctx.send(start, event['summary'])
            print(event['summary'])
            await ctx.send(start)

    @commands.command()
    async def getAllCalendars(self, ctx):
        await ctx.send('Available Calendars:')
        store = file.Storage('credentials.json')
        creds = store.get()
        service = build('calendar', 'v3', http=creds.authorize(Http()))
        calendar_list = service.calendarList().list(pageToken=None).execute()
        for calendar_list_entry in calendar_list['items']:
            await ctx.send(calendar_list_entry['summary'])

    @commands.command()
    async def getCalendarByName(self, ctx, *, calName):
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        store = file.Storage('credentials.json')
        creds = store.get()
        service = build('calendar', 'v3', http=creds.authorize(Http()))
        calendar_list = service.calendarList().list(pageToken=None).execute()
        for calendar_list_entry in calendar_list['items']:
            # print(calendar_list_entry['summary'], '==', calName,': ', str(calendar_list_entry['summary'] == calName))
            if calendar_list_entry['summary'] == calName:
                events_result = service.events().list(calendarId=calendar_list_entry['id'], 
                    timeMin=now, maxResults=3, singleEvents=True, orderBy='startTime').execute()
                events = events_result.get('items', [])
                # print(len(events))
                if not events:
                    await ctx.send('No upcoming events found in ' + calName)
                else:
                    await ctx.send('Upcoming events in ' + calName + ':')    
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    # print('start.get(date): ',event['start'].get('dateTime'), ' Type: ', type(event['start']))
                    # print(event['start'].get('dateTime'))
                    eventTime = parse(event['start'].get('dateTime'))
                    monthStr = eventTime.strftime("%B")
                    printedTime = monthStr + ' ' + str(eventTime.day) + ', ' + str(eventTime.year)
                    # await ctx.send(start, event['summary'])
                    # print(event['summary'])
                    await ctx.send(printedTime)
                    await ctx.send(event['summary'])       

# add this cog to the bot
def setup(bot):
    bot.add_cog(CalendarCog(bot))
