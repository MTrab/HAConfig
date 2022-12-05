# Imports
import logging

from bs4 import BeautifulSoup
import calendar
import datetime
import requests

_LOGGER = logging.getLogger(__name__)

# Const
# URLs and Page_id
BASE_URL = "https://www.greentel.dk"
GET_DETAILS_PAGE_ID = 6297
GET_DETAILS_PAGE_URL = "/umbraco/api/MyPageApi/GetConsumptionDetails"
GET_INFO_PAGE_ID = 6292
GET_INFO_PAGE_URL = "/umbraco/Surface/MyPage/GetInfo"
GET_PACKAGE_PAGE_URL = "/umbraco/api/MyPageApi/GetPackageGauge"

# Input fields
INPUT_TOKEN = "__RequestVerificationToken"
INPUT_PHONE_NO = "PhoneNo"
INPUT_PASSWORD = "Password"

# Payload keys
PL_DATE_FROM = "FromDate"
PL_DATE_TO = "ToDate"
PL_PAGE_ID = "PageId"
PL_PHONE_NO = "PhoneNo"
PL_TOKEN = "Token"

# Response keys
R_ACCOUNT_TYPE = "AccountType"
R_ACTIVE = "Active"
R_AUTO_ADJUST_AMOUNT = "AutoAdjustAmount"
R_BALANCE = "Balance"
R_CALL = "Opkald"
R_CONSUMPTION = "Consumption"
R_DATA = "Data"
R_DESCRIPTION = "Description"
R_EU = "EU"
R_GB = "GB"
R_HOURS = "timers"
R_ITEMS = "Items"
R_LEFT = "AmountLeft"
R_PAYMENT_TYPE = "PaymentType"
R_PHONE_NUMBER = "PhoneNumber"
R_QUANTITY = "Qty"
R_RECHARGE_TICKET_AMOUNT = "RechargeTicketAmount"
R_SUBSCRIPTION = "Subscription"
R_SUBSCRIPTION_DK = "Abonnement"
R_SUCCESS = "Success"
R_TEXT_GAUGE = "TextGauge"
R_TEXT_GAUGE_SPLIT = " brugt<br/>"
R_TOKEN = "Token"
R_TOTAL = "AmountTotal"
R_UNIT = "UnitGauge"
R_USED = "AmountUsed"
R_USER = "User"
R_USERNAME = "Username"

# Labels
L_DATA = "Data"
L_DK = "DK"
L_HOURS = "Timer"
L_SECONDS = "Sekunder"
L_TALK = "Tale"


class greentel:
    def __init__(self, phoneNo, password):
        self._session = requests.Session()
        self._phoneNo = phoneNo
        self._password = password
        self._token = None
        self._data = None
        self._subscriptions = {}
        _LOGGER.debug(f"init: OK")

    def update(self):
        loggedIn = False

        if self._session:
            r = self._getStartPageAsJSON()
            loggedIn = r[R_SUCCESS]

        if not loggedIn:
            loggedIn = self.login()

        _LOGGER.debug(f"update: loggedIn ({loggedIn})")

        # Call the subfunctions and extract the data
        self._fetchSubscriptions()
        self._fetchPackageDetails()
        self._fetchUserDetails()

        return True

    def login(self):
        r = self._session.get(BASE_URL)

        if r.status_code == 200:
            _LOGGER.debug(f"login: website is up")
            # Get the HTML from the main page
            html = BeautifulSoup(r.text, "html.parser")

            # Prepare the payload in a Dict
            payload = {
                INPUT_TOKEN: None,
                INPUT_PHONE_NO: self._phoneNo,
                INPUT_PASSWORD: self._password,
            }

            # Retieve the token from the login form
            for inputTag in html.find_all("input"):
                if inputTag.has_attr("name") and inputTag["name"] == INPUT_TOKEN:
                    payload[INPUT_TOKEN] = inputTag["value"]
                    _LOGGER.debug(f"login: token ({payload[INPUT_TOKEN]})")
                    break

            _LOGGER.debug(
                f"login: logging in with (phonenumber: {self._phoneNo}, password: {self._password})"
            )

            # Send the login details
            r = self._session.post(BASE_URL + html.form["action"], data=payload)

            self._data = self._getStartPageAsJSON()
            if self._responseOK(self._data):
                self._token = self._data[R_DATA][0][R_TOKEN]
                return True

    def getSubscriptions(self):
        return self._subscriptions.values()

    def _fetchSubscriptions(self):
        uniqueSubscriptions = set()
        if self._data:
            # Find unique subscriptions
            for element in self._data[R_DATA]:
                uniqueSubscriptions.add(element[R_SUBSCRIPTION])
            _LOGGER.debug(
                f"_fetchSubscriptions: found {len(uniqueSubscriptions)} subscriptions"
            )

            # Collect the info on the subscriptions
            for name in uniqueSubscriptions:
                sub = subscription(name)
                for element in self._data[R_DATA]:
                    if element[R_SUBSCRIPTION] == name:
                        sub.setActive(element[R_ACTIVE])
                        sub.setBalance(element[R_BALANCE])
                        sub.setPaymentType(element[R_PAYMENT_TYPE])
                        sub.setRechargeTicketAmount(element[R_RECHARGE_TICKET_AMOUNT])
                        sub.setAutoAdjustAmount(element[R_AUTO_ADJUST_AMOUNT])
                        _LOGGER.debug(
                            f'_fetchSubscriptions: found info on the "{name}" subscription'
                        )
                        break
                self._subscriptions[name] = sub

            # Collect the users in the subscriptions
            for user in self._data[R_DATA]:
                self._subscriptions[user[R_SUBSCRIPTION]].addUser(
                    user[R_ACCOUNT_TYPE],
                    user[R_USER][R_USERNAME] if not isinstance(user[R_USER][R_USERNAME], type(None)) else str(user[R_PHONE_NUMBER]),
                    user[R_PHONE_NUMBER],
                )
                _LOGGER.debug(
                    f'_fetchSubscriptions: found info on the user "{user[R_USER][R_USERNAME]}" ({user[R_PHONE_NUMBER]}) subscription'
                )

    def _fetchPackageDetails(self):
        if self._subscriptions:
            payload = {
                PL_PAGE_ID: GET_INFO_PAGE_ID,
                PL_TOKEN: self._token,
            }
            for sub in self._subscriptions.values():
                payload[PL_PHONE_NO] = sub.getUser().getPhoneNo()

                r = self._session.post(
                    BASE_URL + GET_PACKAGE_PAGE_URL, data=payload
                ).json()
                if self._responseOK(r):
                    for element in r[R_DATA][R_CONSUMPTION]:
                        sub.addConsumable(
                            element[R_TEXT_GAUGE].split(R_TEXT_GAUGE_SPLIT)[0],
                            element[R_TOTAL],
                            element[R_USED],
                            element[R_LEFT],
                            element[R_UNIT],
                        )

    def _fetchUserDetails(self):
        if self._subscriptions:
            # Prepare some DATE variables for the payload
            now = datetime.datetime.now()
            year = now.strftime("%Y")
            month = now.strftime("%m")
            payload = {
                PL_PAGE_ID: GET_DETAILS_PAGE_ID,
                PL_TOKEN: self._token,
                PL_DATE_FROM: year + "-" + month + "-01",
                PL_DATE_TO: year
                + "-"
                + month
                + "-"
                + str(calendar.monthrange(int(year), int(month))[1]),
            }
            for sub in self._subscriptions.values():
                for user in sub.getUsers():
                    payload[PL_PHONE_NO] = user.getPhoneNo()

                    r = self._session.get(
                        BASE_URL + GET_DETAILS_PAGE_URL, params=payload
                    ).json()
                    if self._responseOK(r):
                        for consumable in r[R_DATA][R_CONSUMPTION][R_ITEMS]:
                            if consumable[R_DESCRIPTION] != R_SUBSCRIPTION_DK:
                                user.addConsumable(
                                    consumable[R_DESCRIPTION], consumable[R_QUANTITY]
                                )

    # Repeated function testing if the reponse is OK
    # Returns boolean
    def _responseOK(self, response, values={R_SUCCESS, R_DATA}):
        if values.issubset(response):
            return response[R_SUCCESS] and len(response[R_DATA]) > 0
        return False

    # Repeated request to the startpage
    # Returns the response as JSON
    def _getStartPageAsJSON(self):
        payload = {PL_PAGE_ID: GET_INFO_PAGE_ID}
        return self._session.get(BASE_URL + GET_INFO_PAGE_URL, params=payload).json()


class subscription:
    def __init__(self, name):
        self._name = name
        self._active = None
        self._balance = None
        self._paymentType = None
        self._rechargeTicketAmount = None
        self._autoAdjustAmount = None
        self._users = []
        self._consumables = {}

    def setActive(self, val):
        self._active = val

    def setBalance(self, val):
        self._balance = val

    def setPaymentType(self, val):
        self._paymentType = val.lower()

    def setRechargeTicketAmount(self, val):
        self._rechargeTicketAmount = val

    def setAutoAdjustAmount(self, val):
        self._autoAdjustAmount = val

    def getName(self):
        return self._name

    def getActive(self):
        return self._active

    def getBalance(self):
        return self._balance

    def getPaymentType(self):
        return self._paymentType

    def getRechargeTicketAmount(self):
        return self._rechargeTicketAmount

    def getAutoAdjustAmount(self):
        return self._autoAdjustAmount

    def addUser(self, accountType, username, phoneNo):
        self._users.append(user(accountType, username, phoneNo))

    def getUser(self, id=0):
        if self._users:
            return self._users[id]

    def getUsers(self):
        if self._users:
            return self._users

    def addConsumable(self, name, total, used, left, unit):
        if unit == R_GB:
            tmp_name = name
            name = L_DATA
            if R_EU in tmp_name:
                name = name + " " + R_EU
            else:
                name = name + " " + L_DK
        elif unit == R_HOURS:
            unit = L_HOURS
            name = L_TALK
        else:
            name = unit
            used = int(used)
        self._consumables[name] = consumable(name, total, used, left, unit)

    def getConsumables(self):
        return self._consumables.values()


class user:
    def __init__(self, accountType, username, phoneNo):
        self._accountType = accountType
        self._username = username
        self._phoneNo = phoneNo
        self._consumables = {}

    def getUsername(self):
        return self._username

    def getPhoneNo(self):
        return self._phoneNo

    def addConsumable(self, name, used):
        if name == R_CALL:
            unit = L_SECONDS
            h, m, s = used.split(":")
            used = int(h) * 3600 + int(m) * 60 + int(s)
        elif L_DATA in name:
            tmp_list = used.split(" ")
            unit = tmp_list[-1]
            used = tmp_list[0]
        else:
            unit = name

        self._consumables[name] = consumable(name, 0, used, 0, unit)

    def getConsumables(self):
        return self._consumables.values()


class consumable:
    def __init__(self, name, total, used, left, unit):
        self._name = name
        self._total = total
        self._used = used
        self._left = left
        self._unit = unit

    def getName(self):
        return self._name

    def getTotal(self):
        return self._total

    def getUsed(self):
        return self._used

    def getLeft(self):
        return self._left

    def getUnit(self):
        return self._unit
