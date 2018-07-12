from flask import Flask, Blueprint, request
from flask_restplus import Api, Resource, fields
from marshmallow import Schema, fields as ma_fields, post_load
from functools import wraps

app = Flask(__name__)

authorizations = {
	'apikey' : {
		'type' : 'apikey',
		'in'   : 'header',
		'name' : 'X-API-KEY'
	}
}

api = Api(app, authorizations=authorizations)

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None
		if 'X-API-KEY' in request.headers:
			token = request.headers['X-API-KEY']
		if not token:
			return{'message' : 'Token is missing.'}, 401

		if token != 'refuge':
			return {'message': 'Your token is wrong, wrong!!!'}, 401

		#print('TOKEN: {}'.format(token))
		return f(*args, **kwargs)
	return decorated


class Users(object):
	def __init__(self, full_name, username, email, password, confirm_password):
		self.full_name = full_name
		self.username = username
		self.email = email
		self.password = password
		self.confirm_password = confirm_password

	def __repr__(self):
		return '{} is the username.{} is the email.'.format(self.username, self.email)

class UserShema(Schema):
	full_name = ma_fields.String() 
	username = ma_fields.String()
	email = ma_fields.String()
	password = ma_fields.String()
	confirm_password = ma_fields.String()

	@post_load
	def create_user(self, data):
		return Users(**data)

a_user = api.model('Register', {'full_name': fields.String('Your names.'), 'username' : fields.String('Your username'), 'email' : fields.String('Your email'), 'password' : fields.String('password'), 'confirm_password': fields.String('confirm_password')})

registers = []
#python = {'language': 'Rubby', 'id' : 1}
user  = Users(full_name = 'refuge', username='wise', email='wise@gmail.com', password='wise123', confirm_password='wise123')
registers.append(user)



#get methods
@api.route('/register')
class Register(Resource):


#	@api.doc(security='apikey')
#	@token_required
	def get(self):
		schema = UserShema(many=True)
		return schema.dump(registers)

	@api.expect(a_user)
	def post(self):
		schema = UserShema()
		new_lang = schema.load(api.payload)
		registers.append(new_lang.data)
		return {'result' : 'New user added'}, 201




if __name__ == '__main__':
	app.run(debug=True)