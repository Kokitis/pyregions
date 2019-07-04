from pony.orm import Database, PrimaryKey, Set, Required, Optional, StrArray


database_object = Database()


class Namespace(database_object.Entity):
	id = PrimaryKey(int, auto=True)
	codes = Set('Code')
	name = Required(str)
	url = Optional(str)
	wiki = Optional(str)
	description = Optional(str)


class Region(database_object.Entity):
	id = PrimaryKey(int, auto=True)
	name = Required(str, unique=True)
	type = Required(str)
	aliases = Optional(StrArray)
	codes = Set('Code')

	parent = Optional('Region', reverse='subregions')
	subregions = Set('Region', reverse='parent')


class Code(database_object.Entity):
	namespace = Required(Namespace)
	value = Required(str)
	PrimaryKey(namespace, value)

	region = Required(Region)