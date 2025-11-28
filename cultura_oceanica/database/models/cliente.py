from peewee import CharField, DateTimeField, Model
from database.database import db
import datetime


class Cliente (Model):

    nome = CharField()
    email = CharField(unique=True)
    data_criacao = DateTimeField(default=datetime.datetime.now)
    rua = CharField()
    cep = CharField()
    cidade = CharField()
    n_casa = CharField()
    bairro =CharField()
    senha = CharField()


    class Meta:
        database = db

class Produtos (Model): 
    
    foto = CharField()
    nome = CharField()
    marca = CharField()
    categoria = CharField()
    preco_unitario =CharField()
    desc=CharField()
    




    class Meta:
        database = db
        