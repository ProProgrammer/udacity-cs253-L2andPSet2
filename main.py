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

# class TestHandler(webapp2.RequestHandler):
#   def post(self):
#       # q = self.request.get("q")
#       # self.response.write(q)

#       self.response.headers['Content-Type'] = 'text/plain'
#       self.response.write(self.request)

app = webapp2.WSGIApplication([('/', MainHandler),
                            ('/thanks', ThanksHandler)
                            ], debug=True)