# -*- coding: utf-8 -*-

from peewee import *
import datetime

db = MySQLDatabase('lianjia', host='localhost', port=3306, user='root', passwd='1234',
                   charset='utf8')


# define base model
class BaseModel(Model):
    class Meta:
        database = db

class LianjiaInfo(BaseModel):
    url = CharField()
    region1 = CharField()
    region2 = CharField()
    community = CharField()
    deal_time = CharField()
    deal_length = CharField()
    total_price = CharField()
    unit_price = CharField()
    style = CharField()
    floor = CharField()
    size = CharField()
    orientation = CharField()
    build_year = CharField()
    decoration = CharField()
    property_time = CharField()
    elevator = CharField()
    info = TextField()

db.connect()
# db.drop_tables([LianjiaInfo], safe=True)
db.create_tables([LianjiaInfo], safe=True)
