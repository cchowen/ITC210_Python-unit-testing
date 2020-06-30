#!/usr/bin/env python3

from urllib.parse import urljoin

import requests

class API(object):

    def __init__(self, base_url):
        """ Creates the API client.
        Paramaters:
            base_url (str): The base url for the API.
        Returns:
            New API class for testing an API.
        """
        self.base_url = base_url

    def create_task(self, cookie, Text, Date):
        """ Create a new task
        Parameters:
            cookie (str): Pre-authorized cookie
            Text (str): Text/description of the task.
            Date (str): Due date of the task
        Returns:
            Response from the server
        """
        url = urljoin(self.base_url, "api/v1/items")
        data = '{ "Text": "%s", "Date": "%s" }' % (Text, Date)
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'todo-session=' + cookie
        }
        response = requests.request("POST", url, headers=headers, data=data)
        return response

    def read_all_tasks(self, cookie):
        url = urljoin(self.base_url, "api/v1/items")
        payload = {}
        headers = {
            'Cookie': 'todo-session=' + cookie
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response

    def read_task(self, cookie, task_id):
        url = urljoin(self.base_url, f"api/v1/items/{task_id}")
        payload = {}
        headers = {
            'Cookie': 'todo-session=' + cookie
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response

    def update_task(self, cookie, task_id, Done):
        url = urljoin(self.base_url, f"api/v1/items/{task_id}")
        data = '{ "Done": "%s"}' % (Done)
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'todo-session=' + cookie
        }
        response = requests.request("PUT", url, headers=headers, data=data)
        return response

    def delete_task(self, cookie, task_id):
        url = urljoin(self.base_url, f"api/v1/items/{task_id}")
        payload = {}
        headers = {
            'Cookie': 'todo-session=' + cookie
        }
        response = requests.request("DELETE", url, headers=headers, data=payload)
        return response

    def read_current_user(self, cookie):
        url = urljoin(self.base_url, "api/v1/user")
        payload = {}
        headers = {
            'Cookie': 'todo-session=' + cookie
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response

if __name__ == "__main__":
    # Remember, this section of code is for you. Do with
    # it what you will, to see what the code looks like
    # for different requests. You may add more api calls
    # or remove them. I have found that if I add too
    # many `print()`s, the output becomes overloaded and
    # unhelpful, but again, this is personal preference.
    base_url = "http://localhost:1337"
    cookie = "s%3AUHa9OUHESD2ExiruFxhUJCO7ZErC_J1H.CIPhydViN%2Bf48kUSGvbSIVIbW5sApwmUJB5xKzRswSk"
   # task_id = "5ef5132195b2030630fe153a"
    api = API(base_url)
    response = api.read_all_tasks(cookie)
    #response = api.create_task(cookie, "Test the API", "2020-02-20")
    #response = api.update_task(cookie, task_id, "false")
    #response = api.delete_task(cookie, task_id)
    #response = api.read_current_user(cookie)
    print(response.ok)
    print(response.status_code)
    print(response.text)
   # print(response.json())