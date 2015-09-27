#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
from rot13_implementation import rot13
import re

form = """
<form method="post">
    What is your birthday?
    <br>
    <label>
        Month
        <input type='text' name='month' value=%(month)s>
    </label>
    <br>

    <label>
        Day
        <input type='text' name='day' value=%(day)s>
    </label>
    <br>

    <label>
        Year
        <input type='text' name='year' value=%(year)s>
    </label>

    <div style='color: red'>%(error)s</div>
    <br>
    <br>
    <input type="submit">
</form>
"""

form_rot13 = """
<form method="post">
    <h1>
        Enter some text to ROT13
    </h1>
    
    <div>
        <textarea name="text" style="height: 100px; width: 400px;">%(rotInput)s</textarea>
    </div>
    <br>
    
    <input type="submit">
</form>
"""

form_signup = """
<head>
    <title>Sign Up</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
    </style>

  </head>

  <body>
    <h2>Signup</h2>
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%(username)s">
          </td>
          <td class="error">
          %(usernameError)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value="%(password)s">
          </td>
          <td class="error">
            %(passwordError)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify" value="%(verifyPassword)s">
          </td>
          <td class="error">
            %(verifyPasswordError)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%(email)s">
          </td>
          <td class="error">
            %(emailError)s
          </td>
        </tr>
      </table>

      <input type="submit">
    </form>
  </body>
"""

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']
          
def valid_month(month):
    if month.lower().title() in months:
        return month.lower().title()
    else:
        return None

def valid_day(day):
    if day.isdigit():
        if int(day) >= 1 and int(day) <= 31:
            return int(day)
        else:
            return None

def valid_year(year):
    if year and year.isdigit():
        year = int(year)
        if year >= 1900 and year <= 2020:
            return year
        else:
            return None

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)

def valid_verifyPassord(password, verifyPassword):
    return password == verifyPassword

def escape_html(s):
    return cgi.escape(s, quote=True)

class MainHandler(webapp2.RequestHandler):

    def write_form(self, error='', month='', day='', year=''):
        self.response.write(form % {'error': error,
            'month': escape_html(month),
            'day': escape_html(day),
            'year': escape_html(year) })

    def get(self):
        # self.response.headers['Content-Type'] = 'text/plain'
        # self.response.write(form)
        self.write_form()

    def post(self):
        user_month = self.request.get('month')
        validated_month = valid_month(user_month) 

        user_day = self.request.get('day')
        validated_day = valid_day(user_day)
        
        user_year = self.request.get('year')
        validated_year = valid_year(user_year)

        if not (validated_month and validated_day and validated_year):
            self.write_form(error="This doesn't look like valid to me, friend!", month=user_month, day=user_day, year=user_year)
        else:
            self.redirect('/thanks')

class ThanksHandler(webapp2.RequestHandler):

    def get(self):
        self.response.write("Thanks! That's a totally valid day.")

class Rot13Handler(webapp2.RequestHandler):

    def write_form(self, form_rot_input=""):
        self.response.write(form_rot13 % {
            'rotInput': escape_html(form_rot_input)
            })

    def get(self):
        self.write_form()

    def post(self):
        rot_input = self.request.get('text')
        # self.response.write(rot_input)
        # print 'rot_input:', rot_input
        rot_output = rot13(rot_input)
        # self.response.write(rot_output)
        self.write_form(rot_output)

class SignupHandler(webapp2.RequestHandler):

    USERNAME_ERROR = "That's not a valid username"
    PASSWORD_ERROR = "That's not a valid password"
    VERIFY_ERROR = "Your passwords didn't match"
    EMAIL_ERROR = "That's not a valid email"

    def write_form(self, username="", usernameError="", password="", passwordError="", verifyPassword="", verifyPasswordError="", email="", emailError=""):
        self.response.write(form_signup % {
            'username': escape_html(username),
            'usernameError': usernameError,
            'password': escape_html(password),
            'passwordError': passwordError,
            'verifyPassword': escape_html(verifyPassword),
            'verifyPasswordError': verifyPasswordError,
            'email': escape_html(email),
            'emailError': emailError
            })

    def get(self):
        self.write_form()

    def post(self):
        username_input = self.request.get('username')
        password_input = self.request.get('password')
        verifyPassword_input = self.request.get('verify')
        email_input = self.request.get('email')
        errorCheck = False

        displayUsernameError = ""
        displayPasswordError = ""
        displayVerifyError = ""
        displayEmailError = ""

        if not valid_username(username_input):
            displayUsernameError = self.USERNAME_ERROR
            errorCheck = True

        if not valid_password(password_input):
            displayPasswordError = self.PASSWORD_ERROR
            errorCheck = True

        if not valid_verifyPassord(password_input, verifyPassword_input):
            displayVerifyError = self.VERIFY_ERROR
            errorCheck = True

        if email_input:
            if not valid_email(email_input):
                displayEmailError = self.EMAIL_ERROR
                errorCheck = True

        if errorCheck == True:
            self.write_form(username = username_input,
                usernameError = displayUsernameError,
                passwordError = displayPasswordError,
                verifyPasswordError = displayVerifyError,
                email = email_input,
                emailError = displayEmailError)
        else:
            self.redirect('/pset2/welcome?username=%s' % username_input)

        # if not email_input:
        #     if valid_username(username_input) and valid_password(password_input) and valid_verifyPassord(password_input, verifyPassword_input):
        #         self.redirect('/pset2/welcome?username=' + username_input)
        #     elif not (username_input and password_input and verifyPassword_input):
        #         self.write_form(usernameError = USERNAME_ERROR, passwordError = PASSWORD_ERROR)
        #     elif not (valid) 

        # elif not (valid_username and valid_password)



class WelcomeHandler(webapp2.RequestHandler):

    def get(self):
        username_input = self.request.get('username')
        self.response.write('Welcome, %s!' % username_input)


# class TestHandler(webapp2.RequestHandler):
#   def post(self):
#       # q = self.request.get("q")
#       # self.response.write(q)

#       self.response.headers['Content-Type'] = 'text/plain'
#       self.response.write(self.request)

app = webapp2.WSGIApplication([('/', MainHandler),
                            ('/thanks', ThanksHandler),
                            ('/pset2/rot13', Rot13Handler),
                            ('/pset2/signup', SignupHandler),
                            ('/pset2/welcome', WelcomeHandler)
                            ], debug=True)