# app/db.py

import databases
import ormar
import sqlalchemy
import datetime

from .config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"
    id: int = ormar.Integer(primary_key=True)
    email: str = ormar.String(max_length=128, unique=True, nullable=False)
    active: bool = ormar.Boolean(default=True, nullable=False)


class Zones(ormar.Model):
    class Meta(BaseMeta):
        tablename = "zones"
    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=128,nullable=False, default="Zone")
    camera_id: int = ormar.Integer(nullable=False, default=1)
    x: int = ormar.Integer(nullable=False, default=800)
    y: int = ormar.Integer(nullable=False, default=600)


class Cameras(ormar.Model):
    class Meta(BaseMeta):
        tablename = "cameras"
    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=128,nullable=False, default="Camera")
    connectionstring: str = ormar.String(max_length=256,nullable=False)
    threshold: int = ormar.Integer(nullable=True)
    lat:float = ormar.Float(nullable=True)
    long:float = ormar.Float(nullable=True)
    # camera_shift_time: int = ormar.Integer()
    # lastchange: datetime.datetime = ormar.DateTime(default=datetime.datetime.now) 


class PersonInstance(ormar.Model):
    class Meta(BaseMeta):
        tablename = "person_instance"
    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=128,nullable=False, default="PersonInstance")


class Person(ormar.Model):
    class Meta(BaseMeta):
        tablename = "person"
    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=128,nullable=False, default="Person")

#  tracking_obj = {
#                         "camName": cameraName,
#                         "alertTime": my_date.isoformat(),
#                         "subjectId": entity_id,
#                         "location": {
#                             "latInDegrees": lat,
#                             "lonInDegrees": longi
#                         },
#                         "imagePayload":{
#                             "fileName": str(frame_id) + ".jpg",
#                             "data": jpg_as_text,
#                             "mimeType": "image/jpeg",
#                             "size": img_bytes,
#                             "confidence": "1"
#                         },
#                         "createInfo":{
#                             "dateTime": my_date.isoformat(),
#                             "sourceSystemId": "ARMY",
#                             "action": "CREATE",
#                             "userId": "VA System",
#                             "username": "VA System",
#                             "agency": "OTHERS"
#                         },
#                         "updateInfo":{
#                             "dateTime": my_date.isoformat(),
#                             "sourceSystemId": "ARMY",
#                             "action": "CREATE",
#                             "userId": "VA System",
#                             "username": "VA System",
#                             "agency": "OTHERS"
#                         }
#                     }




engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)
