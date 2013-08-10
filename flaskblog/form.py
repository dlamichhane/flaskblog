from flask.ext.wtf import Form, TextField, TextAreaField, SelectField, SelectMultipleField, SubmitField, validators, ValidationError, PasswordField
from models import db, Admin

class LoginForm(Form):
    admin = TextField('Admin', [validators.Required()])
#    password = PasswordField('Password', [])

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        admin = Admin.query.filter_by(userd=self.admin.data).first()
        if admin is None:
            self.admin.errors.append('Unknown admin')
            return False

#        if not admin.check_password(self.password.data):
#            self.password.errors.append('Invalid password')
#            return False

        self.admin = admin
        return True

class PostForm(Form):
    title = TextField("Title", [validators.Required("Please enter the title")])
    text = TextAreaField("Text", [validators.Required("Please provide the content for the title")])
    tag = SelectMultipleField("Tag")
    submit = SubmitField("Create Post")

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        pf = Form.validate(self)
        if not pf:
            return False
        else:
            return True

class TagForm(Form):
  tag = TextField('Tag Name', [validators.Required('Enter tag name')])
  submit = SubmitField("Create Tag")

  def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        Form.__init__(self, *args, **kwargs)

class SearchForm(Form):
    search = TextField('Search', [validators.Required('Enter the text to search')])