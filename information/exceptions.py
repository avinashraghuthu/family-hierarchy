class FamilyError(Exception):

	def __init__(self, message, *args, **kwargs):
		Exception.__init__(self, message, *args, **kwargs)


class InvalidEmailError(FamilyError):

	def __init__(self, message, *args, **kwargs):
		FamilyError.__init__(self, message, *args, **kwargs)


class InvalidMobileError(FamilyError):
	def __init__(self, message, *args, **kwargs):
		FamilyError.__init__(self, message, *args, **kwargs)


class InvalidGenderError(FamilyError):
	def __init__(self, message, *args, **kwargs):
		FamilyError.__init__(self, message, *args, **kwargs)


class InvalidPerson(FamilyError):
	def __init__(self, message, *args, **kwargs):
		FamilyError.__init__(self, message, *args, **kwargs)


class InvalidRelationship(FamilyError):
	def __init__(self, message, *args, **kwargs):
		FamilyError.__init__(self, message, *args, **kwargs)


class LoginFailed(FamilyError):
	def __init__(self, message, *args, **kwargs):
		FamilyError.__init__(self, message, *args, **kwargs)
