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
        """ Read all tasks for the current user 
        Parameters:
            cookie (str): Pre-authorized cookie
        Returns:
            Response from the server
        """
        url = urljoin(self.base_url, "api/v1/items")
        payload = {}
        headers = {
            'Cookie': 'todo-session=' + cookie
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response

    def read_task(self, cookie, task_id):
        """ Fetch a task with the provided task ID
        Parameters:
            cookie (str): Pre-authorized cookie
            task_id (str): The "_id" attribute of a task stored in the database,
            used to find a specific task
        Returns:
            Response from the server
        """ 
        url = urljoin(self.base_url, f"api/v1/items/{task_id}")
        payload = {}
        headers = {
            'Cookie': 'todo-session=' + cookie
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response

    def update_task(self, cookie, task_id, Done):
        """ Update a task with the provided task ID
        Parameters:
            cookie (str): Pre-authorized cookie
            task_id (str): The "_id" attribute of a task stored in the database,
            used to find a specific task
            Done (Boolean): The "Done" attribute of a task, used to indicate whether or not a task
            has been completed
        Returns:
            Response from the server    
        """
        url = urljoin(self.base_url, f"api/v1/items/{task_id}")
        data = '{ "Done": "%s"}' % (Done)
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'todo-session=' + cookie
        }
        response = requests.request("PUT", url, headers=headers, data=data)
        return response

    def delete_task(self, cookie, task_id):
        """ Delete a task with the provided task ID
        Parameters:
            cookie (str): Pre-authorized cookie
            task_id (str): The "_id" attribute of a task stored in the database,
            used to find a specific task
        Returns:
            Response from the server
        """ 
        url = urljoin(self.base_url, f"api/v1/items/{task_id}")
        payload = {}
        headers = {
            'Cookie': 'todo-session=' + cookie
        }
        response = requests.request("DELETE", url, headers=headers, data=payload)
        return response

    def read_current_user(self, cookie):
        """ Fetch the current logged-in user from the database
        Parameters:
            cookie (str): Pre-authorized cookie
        Returns:
            Response from the server
        """
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
    cookie = "s%3AsefxupOftreBbHCfgSfSATY4BEpc6eyk.PSG9PLp0BOGxwypBb3mut7U9pRiafoHGMoTdcn%2F%2BLm4"
    api = API(base_url)
    response = api.read_all_tasks(cookie)
    print(response.ok)
    print(response.status_code)
    print(response.text)
  