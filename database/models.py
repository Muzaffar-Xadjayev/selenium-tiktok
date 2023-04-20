from peewee import *
from data.config import DB_NAME,DB_HOST,DB_PASS,DB_USER,DB_PORT

db=PostgresqlDatabase(database=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)

class BaseModel(Model):
    class Meta:
        database = db

class Users(BaseModel):
    telegram_id = BigIntegerField(primary_key=True)
    full_name = CharField(max_length=500)
    username = CharField(max_length=300,null=True)
    join_date = DateTimeField(formats=["%Y-%m-%d %H:%M"])

    class Meta:
        db_name = 'users'

class Logins(BaseModel):
    username_or_email = CharField(max_length=500,primary_key=True)
    password = CharField(max_length=250)

    class Meta:
        db_name = "Logins"