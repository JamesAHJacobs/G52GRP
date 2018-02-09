'''

Rahul Soni, Psyrs11

This page defines the models DJango will use to store data. These models are :

Institution, which represents a company that would buy licenses for this product

Party, which represent companies that would buy/sell currency

Trade, which represents a trade object and all the appropriate data

Profile, which acts as an extension to the Django User model and allows us to assign users to institutions. It also has
two listeners which ensure a Profile is created when a User is and a Profile is saved when a User is.


'''

from django.db import models
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth.models import User
import datetime
import time
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Institution(models.Model):
    institution_name = models.CharField(max_length=100)
    max_users = models.IntegerField(max_length=3)

    def __str__(self):
        return self.institution_name


class Party(models.Model):
    PartyName = models.CharField(max_length=100)
    PartyPhoneNumber = models.CharField(max_length=10)

    def __str__(self):
        return self.PartyName


class Trade(models.Model):

    '''

    TRADE_PAIRS, TRADE_TYPES AND STATUSES allow us to more strictly handle the options for the relevant fields in Trade
    by only allowing them to be one of a set of values.The first value in each pair represents the stored value, and the
    second one the displayed value.

    '''

    TRADE_PAIRS = (
        ('GBPUSD', 'GBPUSD'),
        ('USDCHF', 'USDCHF'),
        ('USDEUR', 'USDEUR'),
        ('USDCNY', 'USDJPY'),
        ('USDCAD', 'USDCAD'),
    )

    TRADE_TYPES = (
        ('SPOT', 'SPOT'),
        ('OTHER', 'OTHER')
    )

    STATUSES = (
        ('PENDING', 'PENDING'),
        ('AFFIRMED', 'AFFIRMED'),
        ('REJECTED', 'REJECTED')
    )

    '''

    The Trade model is linked to several other models:

    It has a foreign key in the form of institution which determines which company's users will be able to modify it

    It has foreign key relationships with two instances of the party model, one representing the buyer and the other
    representing the seller.

    Because Django automatically gives each model a unique ID, these foreign keys do not need to be used to form a
    composite key, rather they exist to ensure referential integrity (if an institution doesn't exist a trade should be
    in the system that is from that institution).

    '''
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    # TradeID = models.BigIntegerField(max_length=50, default=1)
    BuyerID = models.ForeignKey(Party, on_delete=models.PROTECT, related_name='buyer')
    SellerID = models.ForeignKey(Party, on_delete=models.PROTECT)
    Amount_millions = models.DecimalField(max_digits=100, decimal_places=2)
    CurrencyPair = models.CharField(max_length=6, choices=TRADE_PAIRS)  # validation added, happy Sam?
    Rate = models.DecimalField(max_digits=10, decimal_places=3)
    ModifiedByID = models.BigIntegerField(max_length=50)  # this will be changed to user object in due course
    #ModifiedByName = models.ForeignKey(auth.User.id)  # list of modified by as opposed to one
    TradeType = models.CharField(max_length=6, choices=TRADE_TYPES)  # validation needed. length 4 for 'SPOT'
    # Date = models.DateTimeField(default=None, blank=True, null=True)
    TimePushed = models.BigIntegerField(default=None, blank=True, null=True)
    TimeActioned = models.BigIntegerField(default=None, blank=True, null=True)
    Status = models.CharField(max_length=50, choices=STATUSES)  # validation added just for you sam
    Reason = models.CharField(max_length=100, default=None, blank=True, null=True)  # short reason to describe why rejection

    '''

    This function is used to convert the standard python time format into one that works better with Django and
    the datatables library.

    '''
    def push_to_system(self):
        self.TimePushed = int(round(time.time() * 1000))
        self.save()

    def __str__(self):
        strid = "" + str(self.id)
        return strid


class Profile(models.Model):

    '''

    Convention in Django is to not add fields to the User model that do have relevance to authentication, and so we
    instead create a 1-1 relationship between each instance of the user model to a profile model. In this case the
    profile exists only to specify the user's institution, but if additional functionality needed to be added (for
    example, only allowing a user to approve/reject trades up to a certain value if they are a trainee/new), this is
    where it should be added.

    The Profile has a foreign key in User, and is set to cascade so that it will be removed if the user is removed.
    '''

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True)



    '''

    These receivers simply automate the creation of the Profile model so that it doesn't need to be done manually. The
    post_save signal is a Django default that checks for an instance of User to be calling the save/create method. When
    one does, the appropriate receiver is called.

    '''
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
