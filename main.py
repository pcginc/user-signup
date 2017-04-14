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
import re
import cgi

form='''
<!DOCTYPE html>
<html>
<head>
    <title>Sign Up</title>
</head>
<body>
    <h2>Signup</h2>
    <br>
    <form method="post">
        <table>
            <tr>
                <td>
                Username:
                </td>
                <td>
                    <input type="text" name="username" value=%(username)s>
                </td>
                </td>
                    %(err_username)s
                </td>
            </tr>

            <tr>
                <td>
                    Password:
                </td>
                <td>
                    <input type="password" name="password" value=%(password)s>
                </td>
                <td>
                    %(err_pass)s
                </td>
            </tr>

            <tr>
                <td>
                    Verify Password:
                </td>
                <td>
                    <input type="password" name="verify_pass" value=%(verify_pass)s>
                </td>
                <td>
                    %(err_verifypass)s
                </td>
            </tr>

            <tr>
                <td>
                    Email (optional):
                </td>
                <td>
                    <input type="text" name="email" value =%(email)s>
                </td>
                <td>
                    %(erroremail)s
                </td>
            </tr>
        </table>

        <input type="submit">
    </form>
</body>
</html>
'''

welcome_page = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Unit 2 Signup</title>
    </head>

    <body>
        <h2>Welcome, %(username)s!</h2>
    </body>
    </html>
    '''


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

def escape(s):
   return cgi.escape(s,quote = True)

class Signup(webapp2.RequestHandler):
    def signin(self, username="", password="", verify_pass="", email="", err_username="", err_pass="", err_verifypass="", erroremail=""):
        self.response.write(form%{
                                    "username":escape(username),
                                    "password":escape(password),
                                    "verify_pass":escape(verify_pass),
                                    "email":escape(email),
                                    "err_username":escape(err_username),
                                    "err_pass":escape(err_pass),
                                    "err_verifypass":escape(err_verifypass),
                                    "erroremail":escape(erroremail)})

    def get(self):
        self.signin()

    def post(self):
        error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify_pass = self.request.get('verify_pass')
        email = self.request.get('email')

        err_username = ""
        err_pass = ""
        err_verifypass = ""
        erroremail = ""


        if not valid_username(username):
            err_username = "That's not a valid username"
            self.response.write(err_username)
            error = True

        if not valid_password(password):
            err_pass = "That's not a valid password"
            error = True

        elif password != verify_pass:
            err_verifypass = "Passwords did not match"
            error = True

        if not valid_email(email):
            erroremail = "That's not a valid email"
            error = True

        if error:
            self.signin(username,"","",email,err_username,err_pass,err_verifypass,erroremail)
        else:
            self.redirect('/welcome?username=' + username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')

        if valid_username(username):
            self.response.write(welcome_page%{'username':username})
        else:
            self.redirect(Signup)



app = webapp2.WSGIApplication([
    ('/', Signup),
    ('/welcome', Welcome)
], debug=True)
