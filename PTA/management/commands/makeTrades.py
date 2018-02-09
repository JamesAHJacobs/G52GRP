# Rahul Soni Psyrs11 Team MOD

'''

This command can be run by activating the virtualENV and running python manage.py makeTrades x y.

The x here represents the number of random trades that will be added to the system.

The y here represents the delay (in seconds) the command will place inbetween adding trades to the system. Setting this
to 0 will mean all the trades get added in immediately. Currently this must be an integer value.

'''

from django.core.management.base import BaseCommand, CommandError
from PTA.models import *
from random import randint, uniform


class Command(BaseCommand):
    help = 'Pushes X random trades into the system every Y seconds'

    '''

    By using the Django add_arguments method we automate our error handling, as Django will now create good error
    messages for us, for example if there are insufficient command line arguments.

    '''
    def add_arguments(self, parser):
        parser.add_argument('number_of_trades', type=int)
        parser.add_argument('trade_delay', type=int)

    def handle(self, *args, **options):

        number_of_trades = options['number_of_trades']
        trade_delay = options['trade_delay']

        self.stdout.write(self.style.SUCCESS('Successfully read "%d "' % number_of_trades))

        created_Trades = 0

        while created_Trades < number_of_trades:

            buyerSeed = randint(1, 4)

            sellerSeed = buyerSeed

            while sellerSeed == buyerSeed:
                sellerSeed = randint(1, 4)

            institutionSeed = randint(1, 4)

            amountSeed = float("{0:.2f}".format(uniform(0.5, 5)))

            currencyPairSeed = randint(0, 4)

            def getPair(x):
                return {
                    0: 'GBPUSD',
                    1: 'USDCHF',
                    2: 'USDEUR',
                    3: 'USDCNY',
                    4: 'USDCAD',
                }[x]

            currencyPair = getPair(currencyPairSeed)

            modifiedBySeed = randint(0, 3)

            rateSeed = float("{0:.2f}".format(uniform(0.5, 1.5)))

            timePushed = int(round(time.time() * 1000))

            buyer_party = Party.objects.get(id=buyerSeed)

            seller_party = Party.objects.get(id=sellerSeed)

            institution = Institution.objects.get(id=institutionSeed)

            trade = Trade(Status='PENDING', Amount_millions=amountSeed, TradeType='SPOT', Rate=rateSeed,
                          BuyerID=buyer_party, SellerID=seller_party, institution=institution, CurrencyPair=currencyPair,
                          TimePushed=timePushed,ModifiedByID=modifiedBySeed)
            trade.save()

            self.stdout.write(self.style.SUCCESS('Successfully created trade "%d"' % created_Trades))
            created_Trades += 1

            time.sleep(trade_delay)
