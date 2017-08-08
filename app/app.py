from apistar import App, Include, Route, schema
from apistar.docs import docs_routes
from apistar.statics import static_routes
from apistar.schema import List
from pony import orm
from pony.orm import db_session


db = orm.Database()


class Person(db.Entity):
    name = orm.Required(str)
    age = orm.Required(int)
    cars = orm.Set('Car')


class Car(db.Entity):
    make = orm.Required(str)
    model = orm.Required(str)
    owner = orm.Required(Person)



class PersonSchema(schema.Object):
    properties = {
        'name': schema.String(max_length=100),
        'age': schema.Integer
    }


class CarSchema(schema.Object):
    properties = {
        'make': schema.String(max_length=100),
        'model': schema.String(max_length=50),
        'owner': PersonSchema
    }


def welcome(name=None):
    if name is None:
        return {'message': 'Welcome to API Star!'}
    return {'message': 'Welcome to API Star, %s!' % name}


@db_session
def create_person(person: PersonSchema):
    Person(**person)
    return person


@db_session
def list_persons() -> List[PersonSchema]:
    return [PersonSchema({"name": person.name, "age": person.age}) for person in Person.select()]


@db_session
def create_car(car: CarSchema):
    Car(**car)
    return car


@db_session
def list_cars() -> List[CarSchema]:
    return [CarSchema(**car.__dict__) for car in Car.select()]


routes = [
    Route('/', 'GET', welcome),
    Route('/persons', 'POST', create_person),
    Route('/persons', 'GET', list_persons),
    Route('/cars', 'POST', create_car),
    Route('/cars', 'GET', list_cars),
    Include('/docs', docs_routes),
    Include('/static', static_routes)
]

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
app = App(routes=routes)
