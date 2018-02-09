from django.test import TestCase
from PTA.models import Trade
from PTA.models import Party
from PTA.models import Institution

import time

# The class ModelTestCases contains all tests for the contents of the database, models.py.

class ModelTestCases(TestCase):

    # The setUp method instantiates a trade in the test database, for use in the test cases. The original values given
    # are all valid, but the values are manipulated where necessary depending on the aim of the test.

    def setUp(self):
        self.institution = Institution(institution_name='Trade Affirmers Limited',
                                  max_users=20)

        self.party1 = Party(PartyName='Halifax', PartyPhoneNumber='01225624932')
        self.party2 = Party(PartyName='Hastings Direct', PartyPhoneNumber='0800001066')

        self.trade = Trade(institution=self.institution,
                              BuyerID=self.party1,
                              SellerID=self.party2,
                              Amount_millions= 20.0,
                              CurrencyPair='GBPUSD',
                              Rate=1.24,
                              ModifiedByID=1024,
                              TradeType='SPOT',
                              TimePushed=1491313790,
                              TimeActioned=1491314150,
                              Status='PENDING',
                              Reason=''
                              )

    # The following methods contain each of the test cases for the fields in models.py. Each has a unique name that
    # describes the functionality of the test - for example, test_AmountMillions_Valid tests the performance of a valid
    # value for the AmountMillions field.


    def test_AmountMillions_Valid(self):
        trade = self.trade

        self.assertTrue(trade.Amount_millions,trade.Amount_millions>0 and trade.Amount_millions < 1000000000)

    def test_AmountMillions_Fringe(self):

        trade = self.trade
        trade.Amount_millions = 0.1

        self.assertTrue(trade.Amount_millions > 0 and trade.Amount_millions < 1000000000)

    def test_AmountMillions_Incorrect(self):

        trade = self.trade
        trade.Amount_millions = -10.0

        self.assertFalse(trade.Amount_millions > 0 and trade.Amount_millions < 1000000000)

    def test_AmountMillions_Null(self):

        trade = self.trade
        trade.Amount_millions = 0.0

        self.assertFalse(trade.Amount_millions > 0 and trade.Amount_millions < 1000000000)

    def test_AmountMillions_IncorrectDatatype(self):

        trade = self.trade

        with self.assertRaises(TypeError):
            trade.Amount_millions = "asd"
            self.assertFalse(trade.Amount_millions > 0 and trade.Amount_millions < 1000000000)

    def test_CurrencyPair_Valid(self):

        trade = self.trade

        self.assertIn((trade.CurrencyPair,trade.CurrencyPair), trade.TRADE_PAIRS)

    def test_CurrencyPair_IncorrectLength1(self):

        trade = self.trade
        trade.CurrencyPair = "USDCH"

        self.assertNotIn((trade.CurrencyPair,trade.CurrencyPair), trade.TRADE_PAIRS)

    def test_CurrencyPair_IncorrectLength2(self):

        trade = self.trade
        trade.CurrencyPair = "USDCNYY"

        self.assertNotIn((trade.CurrencyPair,trade.CurrencyPair), trade.TRADE_PAIRS)

    def test_CurrencyPair_IncorrectDatatype(self):

        trade = self.trade

        trade.CurrencyPair = 328289
        self.assertNotIn((trade.CurrencyPair, trade.CurrencyPair), trade.TRADE_PAIRS)

    def test_CurrencyPair_IncorrectCode(self):

        trade = self.trade
        trade.CurrencyPair = "GSBUDS"

        self.assertNotIn((trade.CurrencyPair,trade.CurrencyPair), trade.TRADE_PAIRS)

    def test_Rate_Valid(self):

        trade = self.trade
        trade.Rate = 1.2332

        self.assertTrue(trade.Rate > 0 and len(str(trade.Rate)) <= 11)

    def test_Rate_Out_Of_Range1(self):

        trade = self.trade
        trade.Rate = 349443849834.324423453533

        self.assertFalse(trade.Rate > 0 and len(str(trade.Rate)) <= 11)
        ## <=11 to account for decimal point being counted in len

    def test_Rate_Out_Of_Range2(self):

        trade = self.trade
        trade.Rate = 0.0000

        self.assertFalse(trade.Rate > 0 and len(str(trade.Rate)) <= 11)

    def test_Rate_Out_Of_Range3(self):

        trade = self.trade
        trade.Rate = -31.343

        self.assertFalse(trade.Rate > 0 and len(str(trade.Rate)) <= 11)

    def test_Rate_IncorrectDatatype(self):

        trade = self.trade

        with self.assertRaises(TypeError):
            trade.Rate = "hello"
            self.assertTrue(trade.Rate > 0 and len(str(trade.Rate)) <= 11)

    def test_ModifiedByID_Valid(self):

        trade = self.trade

        self.assertTrue(trade.ModifiedByID > 0 and len(str(trade.ModifiedByID)) <= 10)

    def test_ModifiedByID_Out_Of_Range1(self):

        trade = self.trade
        trade.ModifiedByID = 48328382103213909293123203392393293209

        self.assertFalse(trade.ModifiedByID > 0 and len(str(trade.ModifiedByID)) <= 10)

    def test_ModifiedByID_Out_Of_Range2(self):

        trade = self.trade
        trade.ModifiedByID = -283

        self.assertFalse(trade.ModifiedByID > 0 and len(str(trade.ModifiedByID)) <= 10)

    def test_ModifiedByID_IncorrectDatatype(self):

        trade = self.trade

        with self.assertRaises(TypeError):
            trade.ModifiedByID = [2,29,3,494]
            self.assertTrue(trade.ModifiedByID > 0 and len(str(trade.ModifiedByID)) <= 10)

    def test_TradeType_Valid1(self):

        trade = self.trade

        self.assertIn((trade.TradeType, trade.TradeType), trade.TRADE_TYPES)

    def test_TradeType_Valid2(self):

        trade = self.trade
        trade.TradeType = 'OTHER'

        self.assertIn((trade.TradeType, trade.TradeType), trade.TRADE_TYPES)

    def test_TradeType_Incorrect_Type1(self):

        trade = self.trade
        trade.TradeType = 'SPON'

        self.assertNotIn((trade.TradeType,trade.TradeType), trade.TRADE_TYPES)

    def test_TradeType_Incorrect_Type2(self):

        trade = self.trade
        trade.TradeType = 'DOLPHIN'

        self.assertNotIn((trade.TradeType,trade.TradeType), trade.TRADE_TYPES)

    def test_TimePushed_Valid(self):

        trade = self.trade

        self.assertTrue(trade.TimePushed > 0 and trade.TimePushed < int(time.time()))
        ## second condition asserts that time pushed is not in the future!

    def test_TimePushed_IncorrectTime(self):

        trade = self.trade
        trade.TimePushed = 3155760000 #corresponds to 01 Jan 2070, 00:00:00 GMT

        self.assertFalse(trade.TimePushed > 0 and trade.TimePushed < int(time.time()))

    def test_TimePushed_IncorrectDatatype(self):

        trade = self.trade

        with self.assertRaises(TypeError):
            trade.TimePushed = "John Titor"
            self.assertTrue(trade.TimePushed > 0 and trade.TimePushed < int(time.time()))

    def test_TimeActioned_Valid(self):

        trade = self.trade

        self.assertTrue(trade.TimeActioned > trade.TimePushed and trade.TimeActioned < int(time.time()))
        ## TimeActioned must be after TimePushed and not in the future

    def test_TimeActioned_IncorrectTime1(self):

        trade = self.trade
        trade.TimeActioned = 141306950 # corresponds to 04 April 2017 11:55 - before trade.TimePushed

        self.assertFalse(trade.TimeActioned > trade.TimePushed and trade.TimeActioned < int(time.time()))

    def test_TimeActioned_IncorrectTime2(self):

        trade = self.trade
        trade.TimeActioned = 3155760000 #corresponds to 01 Jan 2070, 00:00:00 GMT

        self.assertFalse(trade.TimeActioned > trade.TimePushed and trade.TimeActioned < int(time.time()))

    def test_TimeActioned_IncorrectDatatype(self):

        trade = self.trade

        with self.assertRaises(TypeError):
            trade.TimeActioned = [4,4,4,4,4,3]
            self.assertTrue(trade.TimeActioned > trade.TimePushed and trade.TimeActioned < int(time.time()))


    def test_Status_Valid1(self):

        trade = self.trade

        self.assertIn((trade.Status, trade.Status), trade.STATUSES)

    def test_Status_Valid2(self):

        trade = self.trade
        trade.Status = 'AFFIRMED'

        self.assertIn((trade.Status, trade.Status), trade.STATUSES)

    def test_Status_Valid3(self):

        trade = self.trade
        trade.Status = 'REJECTED'

        self.assertIn((trade.Status, trade.Status), trade.STATUSES)

    def test_Status_IncorrectType(self):

        trade = self.trade
        trade.Status = 'hello'

        self.assertNotIn((trade.Status, trade.Status), trade.STATUSES)

    def test_Status_IncorrectDatatype(self):

        trade = self.trade

        trade.Status = 123

        self.assertNotIn((trade.Status, trade.Status), trade.STATUSES)

    def test_Reason_Valid1(self):

        trade = self.trade

        if len(trade.Reason) > 0:
            self.assertTrue(len(trade.Reason) > 20 and len(trade.Reason) < 300)
        elif len(trade.Reason) == 0:
            self.assertEquals(trade.Reason, '')

    def test_Reason_Valid2(self):

        trade = self.trade
        trade.Reason = 'Amount millions was erroneous - too high, did not correspond to written documents.'

        if len(trade.Reason) > 0:
            self.assertTrue(len(trade.Reason) > 20 and len(trade.Reason) < 300)
        elif len(trade.Reason) == 0:
            self.assertEquals(trade.Reason, '')

    def test_Reason_TooShort(self):

        trade = self.trade
        trade.Reason = 'Didnt look right.'

        if len(trade.Reason) > 0:
            self.assertFalse(len(trade.Reason) > 20 and len(trade.Reason) < 300)
        elif len(trade.Reason) == 0:
            self.assertEquals(trade.Reason, '')

    def test_Reason_TooLong(self):

        trade = self.trade
        trade.Reason = ' Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed congue tempus tortor quis egestas. Praesent et fermentum nibh. Donec aliquam, nisi a porta malesuada, leo erat volutpat tellus, quis venenatis dui libero ut nulla. Pellentesque egestas mollis viverra. Nam dignissim felis sapien, eu iaculis turpis finibus quis. Vivamus a risus eu orci congue imperdiet. Mauris dapibus cursus nulla, ac consequat justo luctus at. Donec interdum pretium varius. Donec in nunc turpis. Integer urna nibh, vestibulum ut velit nec, rhoncus porttitor turpis. Sed feugiat tortor ac eros malesuada maximus. Nullam eu sem vel ipsum fringilla sagittis. Duis semper sapien posuere, posuere justo sit amet, interdum ipsum. Quisque sed pellentesque nunc. Donec feugiat metus in laoreet fringilla. Nullam iaculis odio in turpis maximus eleifend. Curabitur sed sem mollis lacus rutrum vehicula vitae ac risus. Integer eget accumsan ipsum. Nam ante quam, pretium a pulvinar interdum, convallis ut leo. Proin nulla erat, facilisis nec enim quis, gravida rhoncus neque. Interdum et malesuada fames ac ante ipsum primis in faucibus. Phasellus bibendum scelerisque condimentum. Duis sed tortor ut urna interdum pellentesque at sed velit. Proin dignissim orci ultricies volutpat elementum. Quisque eget urna mollis, mollis massa nec, feugiat ex. Suspendisse dictum, enim id semper facilisis, sem dolor dapibus odio, sed faucibus est felis id lacus. Donec eget magna ultricies, imperdiet tellus ac, varius mi. '

        if len(trade.Reason) > 0:
            self.assertFalse(len(trade.Reason) > 20 and len(trade.Reason) < 300)
        elif len(trade.Reason) == 0:
            self.assertEquals(trade.Reason, '')

    def test_Reason_IncorrectDatatype(self):

        trade = self.trade

        with self.assertRaises(TypeError):
            trade.Reason = 192392
            if len(trade.Reason) > 0:
                self.assertFalse(len(trade.Reason) > 20 and len(trade.Reason) < 300)
            elif len(trade.Reason) == 0:
                self.assertEquals(trade.Reason, '')

    def test_InstitutionName_Valid(self):

        institution = self.institution

        self.assertTrue(len(institution.InstitutionName) > 0 and len(institution.InstitutionName) < 50)

    def test_InstitutionName_TooShort(self):

        institution = self.institution
        institution.InstitutionName = ''

        self.assertFalse(len(institution.InstitutionName) > 0 and len(institution.InstitutionName) < 50)


    def test_InstitutionName_TooLong(self):

        institution = self.institution
        institution.InstitutionName = 'Trade Affirmers Limited based in Bristol United Kingdom with overseas offices in Gambia, US, Australia, Japan, Brazil.'

        self.assertFalse(len(institution.InstitutionName) > 0 and len(institution.InstitutionName) < 50)

    def test_InstitutionName_IncorrectDatatype(self):

        institution = self.institution

        with self.assertRaises(TypeError):
            institution.InstitutionName = 23232
            self.assertTrue(len(institution.InstitutionName) > 0 and len(institution.InstitutionName) < 50)

    def test_InstMaxUsers_Valid(self):

        institution = self.institution

        self.assertTrue(institution.MaxUsers > 0 and institution.MaxUsers < 100000)

    def test_InstMaxUsers_TooSmall(self):

        institution = self.institution

        institution.MaxUsers = 0

        self.assertFalse(institution.MaxUsers > 0 and institution.MaxUsers < 100000)

    def test_InstMaxUsers_TooLarge(self):

        institution = self.institution

        institution.MaxUsers = 4539439934938439

        self.assertFalse(institution.MaxUsers > 0 and institution.MaxUsers < 100000)

    def test_InstMaxUsers_Negative(self):

        institution = self.institution

        institution.MaxUsers = -34

        self.assertFalse(institution.MaxUsers > 0 and institution.MaxUsers < 100000)

    def test_InstMaxUsers_IncorrectDatatype(self):

        institution = self.institution

        with self.assertRaises(TypeError):
            institution.MaxUsers = "asd"
            self.assertTrue(institution.MaxUsers > 0 and institution.MaxUsers < 100000)

    def test_PartyName_Valid(self):

        party = self.party1

        self.assertTrue(len(party.PartyName) > 0 and len(party.PartyName) < 50)

    def test_PartyName_TooShort(self):

        party = self.party1
        party.PartyName = ''

        self.assertFalse(len(party.PartyName) > 0 and len(party.PartyName) < 50)

    def test_PartyName_TooLong(self):

        party = self.party1
        party.PartyName = 'Santandebts Bank PLC Limited Incorporated Registered Company of Moldova'

        self.assertFalse(len(party.PartyName) > 0 and len(party.PartyName) < 50)

    def test_PartyName_IncorrectDatatype(self):

        party = self.party1

        with self.assertRaises(TypeError):
            party.PartyName = 23343.3231
            self.assertTrue(len(party.PartyName) > 0 and len(party.PartyName) < 50)

    def test_PartyPhoneNumber_Valid(self):

        party = self.party1

        self.assertTrue(len(party.PartyPhoneNumber) == 11 and party.PartyPhoneNumber[0] == '0')

    def test_PartyPhoneNumber_TooShort(self):

        party = self.party1
        party.PartyPhoneNumber = '0122562384'

        self.assertFalse(len(party.PartyPhoneNumber) == 11 and party.PartyPhoneNumber[0] == '0')

    def test_PartyPhoneNumber_TooLong(self):

        party = self.party1
        party.PartyPhoneNumber = '029383234344'

        self.assertFalse(len(party.PartyPhoneNumber) == 11 and party.PartyPhoneNumber[0] == '0')

    def test_PartyPhoneNumber_IncorrectFormat(self):

        party = self.party1
        party.PartyPhoneNumber = '12938323434'

        self.assertFalse(len(party.PartyPhoneNumber) == 11 and party.PartyPhoneNumber[0] == '0')

    def test_PartyPhoneNumber_Incorrect_Datatype(self):

        party = self.party1

        with self.assertRaises(TypeError):
            party.PartyPhoneNumber = 18
            self.assertTrue(len(party.PartyPhoneNumber) == 11 and party.PartyPhoneNumber[0] == '0')
