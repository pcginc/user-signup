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
import jinja2

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)




form = """
        <form action="/welcome" method="post">
            <label>Username</label>
                <input type="text" name="username" value="{username}" required/> <font style="color:red">{nameerror}</font>
            <br>
            <label>Password</label>
                <input type="password" name="password1" required/>
            <br>
            <label>Verify Password</label>
                <input type="password" name="password2" required/> <font style="color:red" pattern="">{perror}</font>
            <br>
            <label>Email (optional)</label>
                <input type="email" name="useremail" value="{useremail}"/> <font style="color:red" pattern="">{eerror}</font>
            <br>
            <input type="submit" value="Submit"/>
        </form>
        """.format(username=username, nameerror=usernameerror, perror=passworderror, useremail=useremail, eerror=emailerror)


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)


class Signup(webapp2.RequestHandler):
    def get(self):
        self.response.write(form)

    def post(self):
        error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username, email = email)

        if not valid_username(username):
            params['nameerror'] = "That's not a valid username"
            error = True

        if not valid_password(password):
            params['perror'] = "That's not a valid password"
            error = True

        elif password != verify:
            params['perror'] = "Passwords did not match"
            error = True

        if not valid_email(email):
            params['eerror'] = "That's not a valid email"
            error = True

        if error:
            self.response.write(form, **params)
        else:
            self.redirect('/welcome?username=' + username)

class Welcome(BaseHandler):
    def get(self):
        username = self.request.get('username')
        welcome = """
            <head>
                <title>Unit 2 Signup</title>
            </head>

            <body>
                <h2>Welcome, {{username}}!</h2>
            </body>
            """

        if valid_username(username):
            self.render(Welcome, username = username)
        else:
            self.redirect('/signup')



app = webapp2.WSGIApplication([
    ('/signup', Signup)
    ('/welcome', Welcome)
], debug=True)
