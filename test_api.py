#!/usr/bin/env python3
import random
import string
import unittest

from api import API


def generate_random_text(l=10):
    """ Helper to generate random text for creating new tasks.
    This is helpful and will ensure that when you run your tests,
    a new text string is created. It is also good for determining
    that two tasks are unique.
    Keyword arguments:
        l (int): How long the generated text should be (default 10)
    Returns:
        A randomly-generated string of length `l`
    """
    chars = string.hexdigits
    return "".join(random.choice(chars) for i in range(l)).lower()


def generate_random_date(year=None, month=None, date=None):
    """ Helper to generate random date for creating new tasks.
    This is helpful as another way of generating random tasks
    Keyword arguments:
        year: Specify a year (default None)
        month: Specify a month (default None)
        date: Specify a date (default None)
    Returns:
        A randomly-generated string representation of a date
    """
    if not year:
        year = str(random.randint(2000, 2025))
    if not month:
        month = str(random.randint(1, 12))
    if not date:
        date = str(random.randint(1, 28))
    return str(year) + "-" + str(month) + "-" + str(date)



class TestAPI(unittest.TestCase):

    # update these two values with your own.
    base_url = "http://localhost:1337"
    cookie = "s%3AsefxupOftreBbHCfgSfSATY4BEpc6eyk.PSG9PLp0BOGxwypBb3mut7U9pRiafoHGMoTdcn%2F%2BLm4"

    # This will be run once, when you start your tests.
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.api = API(self.base_url)

    def test_create_task(self):
        """ Tests creating a task is successful.
        This is an example test:
            - Create the task w/dummy data
            - Verify that the task was created
            - Delete the task we created
        You will be required to implement the other tests
        that are defined in BaseTestCase. They will be marked
        with @abc.abstractmethod.
        """
        Text = generate_random_text()
        Date = generate_random_date()


        resp = self.api.create_task(self.cookie, Text, Date)
        self.assertTrue(resp.ok, msg=f"The Create Task failed: {resp.reason}.")
        task = resp.json()
        self.assertEqual(task["Text"], Text, msg="The task's Text did not match the expected Text.")
        self.assertEqual(task["Date"], Date, msg="The task's Date did not match the expected Date.")
        self.assertFalse(task["Done"], msg="The task's Done returned True, expected False.")

        # cleanup - we don't want to conflict with other tests
        # or have a test task in our database.
        self.api.delete_task(self.cookie, task["_id"])

    def test_read_one_task(self):
        Text = generate_random_text()
        Date = generate_random_date()

        resp = self.api.create_task(self.cookie, Text, Date)
        task = resp.json()
        resp = self.api.read_task(self.cookie, task["_id"])
        task = resp.json()
        self.assertEqual(task["Text"], Text, msg="The read task has the wrong text.")
        self.assertEqual(task["Date"], Date, msg="The read task has the wrong date.")
        self.assertFalse(task["Done"], msg="The read task says it's true (expected false).")
        self.api.delete_task(self.cookie, task["_id"])


    def test_read_all_tasks(self):
        for x in range(3):
            Text = generate_random_text()
            Date = generate_random_date()
            self.api.create_task(self.cookie, Text, Date)
        resp = self.api.read_all_tasks(self.cookie)
        tasklist = resp.json()
        user_id = tasklist[0]["UserId"]
        for task in tasklist:
            self.assertEqual(task["UserId"], user_id, msg="A task returned an unexpected UserId.")
            self.api.delete_task(self.cookie, task["_id"])
           

    
    def test_update_task(self):
        Text = generate_random_text()
        Date = generate_random_date()
        resp = self.api.create_task(self.cookie, Text, Date)
        task = resp.json()
        if task["Done"] == False:
            Done = 1
        else:
            Done = 0
        resp = self.api.update_task(self.cookie, task["_id"], Done)
        task = resp.json()
        self.assertEqual(task["Done"], Done, msg="The task returned a value other than the one provided by update_task.")
        self.api.delete_task(self.cookie, task["_id"])

    
    
    def test_delete_task(self):
        Text = generate_random_text()
        Date = generate_random_date()
        resp = self.api.create_task(self.cookie, Text, Date)
        task = resp.json()
        current_task = task["_id"]
        self.api.delete_task(self.cookie, task["_id"])
        self.assertTrue(resp.ok, msg="The delete function failed")
        response = self.api.read_task(self.cookie, current_task)
        self.assertFalse(response.ok,msg="Attempt to read a deleted task succeeded illegally.")

    def test_read_current_user(self):
        resp = self.api.read_current_user(self.cookie)
        user = resp.json()
        self.assertIn("Id", user, msg="No ID field found in user data")
        self.assertIn("UserName", user, msg="No UserName field found in user data")
        self.assertIn("Email", user, msg="No Email field found in user data")


    # Make more methods that begin with 'test` to test all endpoints
    # properly work and fail when you expect them to.

    def test_invalid_read_one(self):
        fake_id = generate_random_text(l=24).lower()
        response = self.api.read_task(self.cookie, fake_id)
        self.assertEqual(response.status_code, 404, msg="The API returned an unexpected status code (expected 404).")

    
    def test_delete_invalid_task(self):
        fake_id = generate_random_text(l=24).lower()
        response = self.api.delete_task(self.cookie, fake_id)
        self.assertEqual(response.status_code, 404, msg="The API returned an unexpected status code (expected 404).")

    def test_invalid_update(self):
        fake_id = generate_random_text(l=24).lower()
        Done = 1
        response = self.api.update_task(self.cookie, fake_id, Done)
        self.assertEqual(response.status_code, 404, msg="The API returned an unexpected status code (expected 404).")

    def test_delete_invalid_id(self):
        fake_id = generate_random_text(l=12)
        response = self.api.delete_task(self.cookie, fake_id)
        self.assertEqual(response.status_code, 500, msg="The API returned an unexpected status code (expected 500).")

    def test_unauthorized_read(self):
        bad_cookie = ""
        resp = self.api.read_all_tasks(bad_cookie)
        self.assertEqual(resp.status_code, 401, msg="Server authorization error (expected 401 Unauthorized).")

    def test_incomplete_create_task(self):
        Date = generate_random_date()
        Text = generate_random_text()
        bad_task = ""
        bad_date = ""
        resp = self.api.create_task(self.cookie, bad_task, Date)
        self.assertFalse(resp.ok,msg="Task unexpectedly created with no text provided (expected text required).")
        resp1 = self.api.create_task(self.cookie, Text, bad_date)
        self.assertFalse(resp.ok, msg="Task unexpectedly created with no date provided (expected date required).")


# Inside this `if` statement will only run if we call the program as
# the top-level module, i.e. when we run this file, not when we import
# this file
if __name__ == "__main__":
    unittest.main()