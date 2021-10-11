# app/main.py

from fastapi import FastAPI

from app.db import database, User, Zones, Cameras, PersonInstance, Person

from src import track
app = FastAPI(title="Lauretta Built Environment Analytics")


@app.get("/")
async def read_root():
    return await User.objects.all()

@app.get("users")
async def read_users():
    return await User.objects.all()

@app.get("zones")
async def read_zones():
    return await Zones.objects.all()


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
        # await Cameras.objects.get_or_create(name="Zone 1")
        await PersonInstance.objects.get_or_create(name="PersonInstance1")
        await Person.objects.get_or_create(name="Person 1")

        await track.eval_prop()





@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
