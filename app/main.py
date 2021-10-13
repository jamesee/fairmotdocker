# app/main.py

from fastapi import FastAPI

from app.db import database, User, Zones, Cameras, PersonInstance, Person, Zone_Status
from src import track
import itertools

app = FastAPI(title="Lauretta Built Environment Analytics")


@app.get("/")
async def read_root():
    return await User.objects.all()

@app.get("users")
async def read_users():
    return await User.objects.all()

@app.get("zone_status" )
async def read_zone_status(zoneid: int = 0):
    return await Zone_Status.objects.get(zone_id = zoneid)

@app.get("cameras")
async def read_cameras():
    return await Cameras.objects.all()

@app.get("person_instance")
async def read_person_instance():
    return await PersonInstance.objects.all()

@app.get("person")
async def read_person():
    return await Person.objects.all()


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
        # create a dummy entry
        await User.objects.get_or_create(email='test@email.com')
        await Zones.objects.get_or_create(name="Zone 1")
        await Cameras.objects.get_or_create(name="Camera 1",connectionstring='TestVideo17.mp4')
        await camerareader()
        await zonereader()
        await PersonInstance.objects.get_or_create(name="PersonInstance1")
        await Person.objects.get_or_create(name="Person 1")
        await track.eval_prop()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()



async def camerareader():

    f = open("cameras.txt", "r")
    camera_list = f.readlines()
    f.close()
    for element in itertools.cycle(camera_list):
        element = element.split(",")

        await Cameras.objects.get_or_create(name=element[0],connectionstring=element[1],threshold=int(element[2]),lat=float(element[3]),long=float(element[4]))
    return 0

async def zonereader():

    f = open("zones.txt", "r")
    zone_list = f.readlines()
    f.close()

    for element in itertools.cycle(zone_list):
        element = element.split(",")

        await Zones.objects.get_or_create(name=element[0],camera_id=int(element[1]),x=int(element[2]),y=int(element[3]))
    return 0

    