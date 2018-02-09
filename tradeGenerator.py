# to run this file
# 1. use python manage.py shell in console
# 2. use exec(open("./tradeGenerator.py").read()) in shell (fill the address of this file in open())

from PTA.models import *
import time
import random

'''

Rahul Soni, Psyrs11

This file has been deprecated in favour of creating a custom Django command which is a better way to do this than
shoving the output of a script into the shell, but I'll keep it around just in case.

'''
randIns = random.randint(1,3)
ins = Institution.objects.get(pk=randIns)

randBuyer = random.randint(1,3)
buy = Party.objects.get(pk=randBuyer)

randSeller = random.randint(1,3)
sell = Party.objects.get(pk=randSeller)

t = Trade(institution=ins,
          BuyerID=buy,
          SellerID=sell,
          Amount_millions=random.uniform(1,10),
          CurrencyPair="USDJPY",
          Rate=random.uniform(0,2),
          ModifiedByID=1,
          TradeType="SPOT",
          TimePushed=int(round(time.time() * 1000)),
          Status="PENDING")

t.save()
