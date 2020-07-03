<h1>How to use these scripts</h1>

The api.py file defines the CRUD operations which interact with an API hosted at the listed address. Using the *requests* module, a provided URL, and a pre-authorized cookie, it makes authenticated HTTP requests to the server, which are then called and used by test_api.py to perform unit tests on the API.

<h2>How to use a pre-authorized cookie</h2>
Because the API uses Google Authentication, you will need to provide a cookie to authorize the Python script when making HTTP requests. Do this by definining the cookie in both the api.py and test_api.py files. 

<h2>How to get a pre-authorized cookie</h2>
You can obtain an authorized cookie by logging into the to-do website. Since the liver server infrastructure is down, this is now done locally. 
  Note that this can be done with only the back-end code (lab-5B) running, but the front-end (vue-5B) presents a nice user interface. 
With lab-5B and vue-5B running, navigate to the project webpage at http://localhost:1337/api/v1/auth/google or http://localhost:8080/login. You will prompted to log in via Google. Make sure you do so with the Google Account previously registered with the Azure database of users from previous projects.
Once you have logged in and are presented with your very own (probably empty) task list, open your web browser's dev tools (this can easily be done with the F12 key). 
Navigate to the Application tab of the developer tools.
Go to the Storage sub-section on the left and click on the "Cookies" drop-down menu.
The cookies we want will be stored at http://localhost:8080. Click that entry.
The cookie we're after is named "todo-session." Select the value of this cookie and copy it to your clipboard.
Paste the value of the cookie into the definition of cookie in both api.py and test_api.py.
Congratulations, your script is now authorized to make HTTP requests! Note that if you log out and back in, you'll need to get a new cookie and update the script again. 

<h2>How to run the code</h2>
To run one of these files, open a terminal and navigate to the directory for this projecting (opening the folder in Visual Studio Code is the easiest way to do this). Once in this directory, you can run either script by prefacing the script name with "python" like so:

<pre><code>python api.py</pre></code>
<pre><code>python test_api.py</pre></code>

That's it! The terminal will then output the results of the script, making it easy to see what happened and whether or not it worked. If you receive a 401 Unauthorized error, it means you need to refresh the cookie in one or both of the scripts. 

For further development, almost all new functionality should change the test_api.py file, as it contains the unit tests. The api.py file should be left alone unless you intend to add a new endpoint to the API. Currently only CRUD operations on the task list and reading the current user are supported, so unless you plan to do more than this, all of your changes should go in test_api.py.

Thanks for reading and happy testing!
