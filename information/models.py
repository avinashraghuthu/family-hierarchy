from __future__ import unicode_literals

from django.db import models

from utils import generate_unique_id, gen_hash_pwd
# Create your models here.


class Base(models.Model):
	created_on = models.DateTimeField(auto_now_add=True, db_index=True)
	updated_on = models.DateTimeField(auto_now=True, db_index=True)

	class Meta:
		abstract = True


class FamilyInfoManager(models.Manager):

	def create_family(self, name, display_name):
		family_id = generate_unique_id('FM')
		family_obj = self.model(family_id=family_id, name=name, display_name=display_name)
		family_obj.save()
		return family_obj


class FamilyInfo(Base):

	family_id = models.CharField(max_length=255, primary_key=True)
	name = models.Charfield(max_length=255)
	display_name = models.Charfield(max_length=255)

	objects = FamilyInfoManager()

	def __unicode__(self):
		return str(self.name) + ' ' + str(self.display_name)

	def serializer(self):
		data = dict()
		data['family_id'] = self.family_id
		data['name'] = self.name
		data['display_name'] = self.display_name
		return data


class RelationshipManager(models.Manager):

	def create_relationship(self, name, display_name, family_id):
		relationship_obj = self.model(name=name, display_name=display_name, family_info=family_id)
		relationship_obj.save()
		return relationship_obj

	def get_relationship(self, name, family_id):
		try:
			obj = self.get(name=name, family_info=family_id)
		except Relationship.DoesNotExist, e:
			obj = None
		return obj


class Relationship(Base):

	name = models.Charfield(max_length=255)
	display_name = models.Charfield(max_length=255)
	family_info = models.ForeignKey(FamilyInfo)

	objects = RelationshipManager()

	def __unicode__(self):
		return str(self.name) + ' ' + str(self.display_name) + ' '


class PersonManager(models.Manager):

	def create_person(self, first_name, last_name, dob, gender, mobile_number, email_id, user_password):
		person_id = generate_unique_id('PER')
		hashed_pwd = gen_hash_pwd(user_password)
		person_obj = self.model(person_id=person_id, first_name=first_name, last_name=last_name,
								dob=dob, gender=gender, mobile_number=mobile_number,
								email_id=email_id, user_password=hashed_pwd)
		person_obj.save()
		return person_obj

	def get_person(self, person_id):
		try:
			obj = self.get(pk=person_id)
		except Person.DoesNotExist, e:
			obj = None
		return obj

	def get_person_by_num(self, mob_number):
		try:
			obj = self.get(mobile_number=mob_number)
		except Person.DoesNotExist, e:
			obj = None
		return obj


class Person(Base):
	GENDER = (
		('Male', 'Male'),
		('Female', 'Female'),
		('Other', 'Other'),
	)

	person_id = models.Charfield(max_length=255, primary_key=True)
	first_name = models.Charfield(max_length=255)
	last_name = models.Charfield(max_length=255)
	dob = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
	gender = models.CharField(max_length=20, choices=GENDER)
	mobile_number = models.CharField(max_length=255, db_index=True, editable=True)
	email_id = models.EmailField(max_length=255, db_index=True, null=True, blank=True, editable=True)
	user_password = models.TextField(max_length=255)
	relatives = models.ManyToManyField('Relatives')
	family_info = models.ForeignKey(FamilyInfo)

	objects = PersonManager()

	def __unicode__(self):
		return str(self.first_name) + ' ' + str(self.last_name) + str(self.email_id)

	def add_relatives(self, relative_obj):
		self.relatives.add(relative_obj)

	def search_relatives(self, relation_name):
		relatives_list = self.relatives.select_related('relationship').all()
		result_list = list()
		for relative in relatives_list:
			if relative.name.lower() == relation_name.lower():
				result_list.append(relative.person)
		return result_list

	def serializer(self):
		data = dict()
		data['person_id'] = self.person_id
		data['first_name'] = self.first_name
		data['last_name'] = self.last_name
		data['dob'] = self.dob
		data['gender'] = self.gender
		data['mobile_number'] = self.mobile_number
		return data



class RelativesManager(models.Manager):

	def create_relatives(self, relative_person, relationship):
		obj = self.model(person= relative_person, relationship=relationship)
		obj.save()
		return obj


class Relatives(models.Model):

	person = models.ForeignKey(Person)
	relationship = models.ForeignKey(Relationship)

	objects = RelativesManager()

	def __unicode__(self):
		return str(self.person) + ' ' + str(self.relationship)





