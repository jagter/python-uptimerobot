#!/usr/bin/env python

import requests
from urllib.parse import quote


class UptimeRobot(object):
    def __init__(self, apiKey, url=None):
        self.apiKey = apiKey

        if url is None:
            self.baseUrl = "https://api.uptimerobot.com/v2/"

    def _request(self, req, parameters=None):

        payload = "api_key={0}&format=json&logs=1".format(self.apiKey)
        url = self.baseUrl + str(req)

        if parameters is not None:
            payload += parameters

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'cache-control': 'no-cache'
        }

        try:
            post_req = requests.post(url, data=payload, headers=headers)

            if not post_req.status_code == 200:
                return 'Error: unexpected response {}'.format(post_req.status_code)
            else:
                return post_req.json()
        except requests.exceptions.RequestException as e:
            return 'Error: {}'.format(e)

    def getMonitors(self):
        """
        Returns status and response payload for all known monitors.
        """
        return self._request('/getMonitors')

    def getMonitorByName(self, friendlyName):
        """
        Returns monitor by name
        """

        req = self._request('/getMonitors')

        for item in req['monitors']:
            if item['friendly_name'] == friendlyName:
                return item

        return 'Error: monitor not found'

    def getMonitorById(self, monitorId):
        """
        Returns the monitor by ID
        """

        req = self._request('/getMonitors')

        for item in req['monitors']:
            if item['id'] == monitorId:
                return item

        return 'Error: monitor not found'

    def newMonitor(self, friendly_name, type, url, **kwargs):

        url_encode = self.__url_to_html(url)
        friendly_name_encode = self.__url_to_html(friendly_name)

        new_monitor = "&friendly_name={0}&type={1}&url={2}".format(friendly_name_encode, type, url_encode)

        if kwargs is not None:
            for k, v in kwargs.items():
                new_monitor += "&{}={}".format(k, v)

        req = self._request('/newMonitor', new_monitor)

        return req

    def editMonitor(self, monid, **kwargs):

        edit_monitor = "&id={0}".format(monid)

        if kwargs is not None:
            for k, v in kwargs.items():
                edit_monitor += "&{}={}".format(k, v)

        req = self._request('/editMonitor', edit_monitor)

        return edit_monitor

    def __url_to_html(self, inputstring):

        return quote(inputstring, safe='')

        # def editMonitor(self, monitorID, monitorStatus=None, monitorFriendlyName=None, monitorURL=None, monitorType=None,
        #                 monitorSubType=None, monitorPort=None, monitorKeywordType=None, monitorKeywordValue=None,
        #                 monitorHTTPUsername=None, monitorHTTPPassword=None, monitorAlertContacts=None):
        #     """
        #     monitorID is the only required object. All others are optional and must be quoted.
        #     Returns Response object from api.
        #     """
        #
        #     url = self.baseUrl
        #     url += "editMonitor?apiKey=%s" % self.apiKey
        #     url += "&monitorID=%s" % monitorID
        #     if monitorStatus:
        #         # Pause, Start Montir
        #         url += "&monitorStatus=%s" % monitorStatus
        #     if monitorFriendlyName:
        #         # Update their FriendlyName
        #         url += "&monitorFriendlyName=%s" % monitorFriendlyName
        #     if monitorURL:
        #         # Edit the MontiorUrl
        #         url += "&monitorURL=%s" % monitorURL
        #     if monitorType:
        #         # Edit the type of montior
        #         url += "&monitorType=%s" % monitorType
        #     if monitorSubType:
        #         # Edit the SubType
        #         url += "&monitorSubType=%s" % monitorSubType
        #     if monitorPort:
        #         # Edit the Port
        #         url += "&monitorPort=%s" % monitorPort
        #     if monitorKeywordType:
        #         # Edit the Keyword Type
        #         url += "&monitorKeywordType=%s" % monitorKeywordType
        #     if monitorKeywordValue:
        #         # Edit the Keyword Match
        #         url += "&monitorKeywordValue=%s" % monitorKeywordValue
        #     if monitorHTTPUsername:
        #         # Edit the HTTP Username
        #         url += "&monitorHTTPUsername=%s" % monitorHTTPUsername
        #     if monitorHTTPPassword:
        #         # Edit the HTTP Password
        #         url += "&monitorHTTPPassword=%s" % monitorHTTPPassword
        #     if monitorAlertContacts:
        #         # Edit the contacts
        #         url += "&monitorAlertContacts=%s" % monitorAlertContacts
        #     url += "&noJsonCallback=1&format=json"
        #     success = self.requestApi(url)
        #     return success
        #
        #
        # def deleteMonitorById(self, monitorID):
        #     """
        #     Returns True or False if monitor is deleted
        #     """
        #     url = self.baseUrl
        #     url += "deleteMonitor?apiKey=%s" % self.apiKey
        #     url += "&monitorID=%s" % monitorID
        #     url += "&noJsonCallback=1&format=json"
        #     success, response = self.requestApi(url)
        #     if success:
        #         return True
        #     else:
        #         return False
        #
        #
        # def requestApi(self, url):
        #     response = urllib_request.urlopen(url)
        #     content = response.read().decode('utf-8')
        #     jContent = json.loads(content)
        #     if jContent.get('stat'):
        #         stat = jContent.get('stat')
        #         if stat == "ok":
        #             return True, jContent
        #     return False, jContent
        #
        # def getAlertContacts(self, alertContacts=None, offset=None, limit=None):
        #         """
        #         Get Alert Contacts
        #         """
        #         url = self.baseUrl
        #         url += "getAlertContacts?apiKey=%s" % self.apiKey
        #         if alertContacts:
        #             url += "&alertContacts=%s" % alertContacts
        #         if offset:
        #             url += "&offset=%s" % offset
        #         if limit:
        #             url += "&limit=%s" % limit
        #         url += "&format=json"
        #         return self.requestApi(url)
        #
        # def getAlertContactIds(self, urlFormat=False):
        #     ids = []
        #     success, response = self.getAlertContacts()
        #     if success:
        #         alertContacts = response.get('alertcontacts').get('alertcontact')
        #         for alertContact in alertContacts:
        #             ids.append(alertContact.get('id'))
        #     if urlFormat:
        #         formatted = ""
        #         for id in ids:
        #             formatted += id + "-"
        #         return formatted[:-1]
        #     else:
        #         return ids
        #
        # def getMonitorId(self, name):
        #     success, response = self.getMonitors()
        #     if success:
        #         monitors = response.get('monitors').get('monitor')
        #         for monitor in monitors:
        #             if monitor['friendlyname'] == name:
        #                 return monitor['id']
        #     return None
        #
        # def deleteMonitorByName(self, name):
        #     return self.deleteMonitorById(self.getMonitorId(name))
