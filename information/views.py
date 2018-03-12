from django.shortcuts import render
from django.views.generic import View
import re
from models import *
from exceptions import (InvalidEmailError, InvalidGenderError,
						InvalidMobileError, FamilyError, InvalidPerson, InvalidRelationship,
						LoginFailed)
from constants import (STR_INVALID_EMAIL, STR_INVALID_GENDER,
						STR_INVALID_MOBILE, STR_RELATIONSHIP_ADDITION_SUCCESS,
						STR_FAMILY_ADDITION_SUCCESS, STR_INVALID_PERSON,
					   STR_INVALID_RELATIONSHIP, STR_RELATIVES_ADDITION_SUCCESS, STR_SEARCH_SUCCESS,
					   STR_LOGIN_SUCCESS, STR_REGISTRATION_SUCCESS, STR_LOGIN_FAILED)
from utils import send_200, send_400, send_201
# Create your views here.


class Register(View):

	def __init__(self):
		self.response = {
			'res_str' : STR_REGISTRATION_SUCCESS,
			'res_data' : {}
		}

	def _validate_email(self, email):
		email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
		if not re.match(email_regex, email):
			raise InvalidEmailError(STR_INVALID_EMAIL)

	def _validate_mobile_number(self, mobile_number):
		if not len(mobile_number) == 10 or \
				not mobile_number.isdigit():
			raise InvalidMobileError(STR_INVALID_MOBILE)

	def _validate_gender(self, gender):
		valid_gender_list = dict(Person.GENDER).keys()
		if gender not in valid_gender_list:
			raise InvalidGenderError(STR_INVALID_GENDER)

	def _validate(self, email_id, gender, mobile_number):
		self._validate_email(email_id)
		self._validate_gender(gender)
		self._validate_mobile_number(mobile_number)

	#TODO: Add authention of apis via session token
	def post(self, request, *args, **kwargs):
		req_params = request.POST
		first_name = req_params['first_name']
		last_name = req_params['last_name']
		gender = req_params['gender']
		dob = req_params['dob']
		email_id = req_params['email_id']
		user_password = req_params['password']
		mobile_number = req_params['mobile_number']
		try:
			self._validate(email_id, gender, mobile_number)
			Person.objects.create_person(first_name, last_name, dob, gender, mobile_number, email_id,
										 user_password)
			return send_201(self.response)
		except FamilyError, e:
			self.response['res_str'] = str(e)
			return send_400(self.response)


class Login(View):

	def __init__(self):
		self.response = {
			'res_str': STR_LOGIN_SUCCESS,
			'res_data': {}
		}

	def post(self, request, *args, **kwargs):
		req_params = request.POST
		mobile_number = req_params['mobile_number']
		password = req_params['password']
		person = Person.objects.get_person_by_num(mobile_number)
		try:
			if not person:
				raise InvalidPerson(STR_INVALID_PERSON)
			if person.user_password != gen_hash_pwd(password):
				raise LoginFailed(STR_LOGIN_FAILED)
			# TODO: Add it to redis and mantain session
			return send_200(self.response)
		except FamilyError, e:
			self.response['res_str'] = str(e)
			return send_400(self.response)


class AddFamily(View):

	def __init__(self):
		self.response = {
			'res_str': STR_FAMILY_ADDITION_SUCCESS,
			'res_data': {}
		}

	def post(self, request, *args, **kwargs):
		req_params = request.POST
		name = req_params['name']
		display_name = req_params['display_name']
		family_obj = FamilyInfo.objects.create_family(name, display_name)
		self.response['res_data'] = family_obj.serializer()
		return send_201(self.response)


class AddRelationship(View):

	def __init__(self):
		self.response = {
			'res_str': STR_RELATIONSHIP_ADDITION_SUCCESS,
			'res_data': {}
		}

	def post(self, request, *args, **kwargs):
		req_params = request.POST
		name = req_params['name']
		display_name = req_params['display_name']
		family_id = req_params['family_id']
		Relationship.objects.create_relationship(name, display_name, family_id)
		return send_201(self.response)


class AddRelatives(View):

	def __init__(self):
		self.response = {
			'res_str': STR_RELATIVES_ADDITION_SUCCESS,
			'res_data': {}
		}

	def _validate(self, person_id, relationship_name, relation_person_id):
		person = Person.objects.get_person(person_id)
		if not person:
			raise InvalidPerson(STR_INVALID_PERSON)
		relationship_obj = Relationship.objects.get_relationship(relationship_name, person.family_info)
		if not relationship_obj:
			raise InvalidRelationship(STR_INVALID_RELATIONSHIP)
		relation_person = Person.objects.get_person(relation_person_id)
		if not relation_person:
			raise InvalidPerson(STR_INVALID_PERSON)
		return person, relationship_obj, relation_person

	def post(self, request, *args, **kwargs):
		req_params = request.POST
		person_id = req_params['person_id']
		relationship_name = req_params['relationship_name']
		relation_person_id = req_params['relation_person_id']
		try:
			person, relationship_obj, relation_person = self._validate(person_id,
											relationship_name, relation_person_id)
			relative_obj = Relatives.objects.create_relatives(relation_person, relationship_obj)
			person.add_relatives(relative_obj)
			return send_200(self.response)
		except FamilyError, e:
			self.response['res_str'] = str(e)
			return send_400(self.response)


class SearchRelatives(View):

	def __init__(self):
		self.response = {
			'res_str': STR_SEARCH_SUCCESS,
			'res_data': []
		}

	def get(self, request, *args, **kwargs):
		req_params = request.POST
		person_id = req_params['person_id']
		relation_name = req_params['relation_name']
		try:
			person = Person.objects.get_person(person_id)
			if not person:
				raise InvalidPerson(STR_INVALID_PERSON)
			relative_persons = person.search_relatives(relation_name)
			person_list = []
			for relative_person in relative_persons:
				person_list.append(relative_person.serializer())
			self.response['res_data'] = person_list
			return send_200(self.response)
		except FamilyError, e:
			self.response['res_str'] = str(e)
			return send_400(self.response)






