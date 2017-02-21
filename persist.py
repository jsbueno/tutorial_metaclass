
class Field:
    def __set__(self, instance, value):
        instance.__dict__[self.name] = value
    def __get__(self, instance, owner):
        if instance:
            return instance.__dict__[self.name]
        return self
    def __del__(self, instance):
        del instance.__dict__[self.name]


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


class ModelBase(type):
    def __new__(metacls, name, bases, namespace):
        for attr_name, value in namespace.items():
            if isinstance(value, Field):
                value.name = attr_name
        return super().__new__(metacls, name, bases, namespace)


class Pessoa(metaclass=ModelBase):

    nome = StrField()
    idade = IntField()
    endereco = StrField()
