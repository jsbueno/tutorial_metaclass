import uuid

class Field:
    def __set__(self, instance, value):
        instance.__dict__[self.name] = value
    def __get__(self, instance, owner):
        if instance:
            return instance.__dict__[self.name]
        return self

    def __del__(self, instance):
        del instance.__dict__[self.name]

    def serialize(self, instance):
        return self.__get__(instance, None)


class StrField(Field):
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} field can only contain strings")
        super().__set__(instance, value)


class IntField(Field):
    def __set__(self, instance, value):
        try:
            value = int(value)
        except ValueError:
            raise TypeError(f"{self.name} field value must be convertible to int")
        super().__set__(instance, value)

class UUIDField(Field):
    def __set__(self, instance, value):
        if isinstance(value, str):
            value = uuid.UUID(str)
        super().__set__(instance, value)

    def serialize(self, instance):
        value = super().serialize(instance)
        return str(value)


def model_setattr(self, attr, value):
    """ Filter __setattribute__ method to avoid that
    any attribute that is not defined as a persistent
    property is ever set.
    """
    if not hasattr(self.__class__, attr):
       raise TypeError(f"{attr} is not a valid attribute for {self.__class__} objects")
    object.__setattr__(self, attr, value)


class ModelBase(type):
    def __new__(metacls, name, bases, namespace):
        for attr_name, value in namespace.items():
            if isinstance(value, Field):
                value.name = attr_name
        if not "__setattr__" in namespace:
            namespace["__setattr__"] = model_setattr

        return super().__new__(metacls, name, bases, namespace)


class Model(metaclass=ModelBase):
    id = UUIDField()

    def __init__(self):
        self.id = uuid.uuid4()


class Pessoa(Model):

    nome = StrField()
    idade = IntField()
    endereco = StrField()
