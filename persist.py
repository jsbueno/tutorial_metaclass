
class Field:
    def __set__(self, instance, value):
        instance.__dict__[self.name] = value
    def __get__(self, instance, owner):
        if instance:
            return instance.__dict__[self.name]
        return self
    def __del__(self, instance):
        del instance.__dict__[self.name]



class Pessoa:

    nome = StrField()
    idade = IntField()
    endereco = StrField()
