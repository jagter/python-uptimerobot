import requests
import json
from urllib.parse import quote


class UptimeRobot(object):
    def __init__(self, apiKey, url=None):
        self.apiKey = apiKey

        if url is None:
            self.baseUrl = "https://api.uptimerobot.com/v2/"

    def __perform_request(self, req, parameters=None):

        payload = {'api_key': self.apiKey, 'format': 'json', 'logs': 1}

        url = self.baseUrl + str(req)

        if parameters is not None:
            for k, v in parameters.items():
                update_parameters = {k: v}
                payload.update(update_parameters)

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
        return self.__perform_request('/getMonitors')

    def getMonitorByName(self, friendlyName):
        """
        Returns monitor by name
        """

        req = self.__perform_request('/getMonitors')

        for item in req['monitors']:
            if item['friendly_name'] == friendlyName:
                return json.dumps(item)

        return json.dumps(dict({'stat': 'fail', 'message': 'monitor not found'}))

    def getMonitorById(self, monitorId):
        """
        Returns the monitor by ID
        """

        req = self.__perform_request('/getMonitors')

        for item in req['monitors']:
            if item['id'] == monitorId:
                return json.dumps(item)

        return json.dumps(dict({'stat': 'fail', 'message': 'monitor not found'}))

    def newMonitor(self, friendly_name, type, url, **kwargs):

        new_monitor = {'friendly_name': self.__url_to_html(friendly_name), 'type': type,
                       'url': self.__url_to_html(url)}

        if kwargs:
            for k, v in kwargs.items():
                update_kwargs = {k: self.__url_to_html(v)}
                new_monitor.update(update_kwargs)

        return self.__perform_request('/newMonitor', new_monitor)

    def editMonitor(self, monid, **kwargs):

        edit_monitor = {'id': monid}

        if kwargs:
            for k, v in kwargs.items():
                update_kwargs = {k: self.__url_to_html(v)}
                edit_monitor.update(update_kwargs)

        return self.__perform_request('/editMonitor', edit_monitor)

    def __url_to_html(self, inputstring):

        return quote(inputstring, safe='')

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