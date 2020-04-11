#Stephen Duncanson
#/u/UCONN_BOOKSTORE
#Reddit Bot Test

import praw
import random
import time

deals=[	"Microsoft Office 2019 only $39.95 | Adobe & more.",
		"Shop 2019 holiday ornaments before they're gone…",
		"Savings, Savings, & Savings for YOU!",
		"🎁 Our GIFT to you: 25% OFF",
		"Happy Thanksgiving!! Give $10 to your parents",
		"Happy Thanksgiving!! Thank Your Parents With $10",
		"HURRY! 30% Off Cold Weather Styles Is Almost GONE",
		"ENDS TODAY: 30% off Sweats & More",
		"30% off is happening now!! (Yes…30% off!)",
		"Pre-Black Friday Deals are HERE!",
		"Your FIRST LOOK at Cyber Deals 😄",
		"LAST CHANCE to shop our Champion Sale!!",
		"🏈 We face East Carolina Soon!",
		"Your favorite brands are STILL on sale!",
		"Sustainable styles you'll love. . .",
		"🍂 25% Off Fall Savings!",
		"Understand your world as you shape it with The Times.",
		"Introducing: UCONN x tokyodachi®",
		"20% off Active Gear for the New School Year"
		"Gifts starting at $10 now in your Urban Outfitters campus shop",
		"Things to do before you leave campus…",
		"Here is your Finals Week Checklist…",
		"Microsoft Office 2019 only $39.95 | Adobe & more.",
		"Shop 2019 holiday ornaments before they're gone…",
		"Savings, Savings, & Savings for YOU!",
		"😎 MORNING CYBER SUNDAY SAVINGS"]


reddit = praw.Reddit(client_id='=',
                     client_secret='',
                     password='',
                     user_agent='',
                     username='')

subreddit = reddit.subreddit('uconn')

while True:
	hot_uconn = subreddit.hot()
	for submission in hot_uconn:
		time.sleep(600)
		print(submission.title)
		submission.reply(random.choice(deals))
		print("Replied!")
