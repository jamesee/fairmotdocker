# app/main.py

from fastapi import FastAPI

from app.db import database, User, Zones

from app.FairMOT.src import track
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


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    await User.objects.get_or_create(email="test@test.com")
    await Zones.objects.get_or_create(name="Zone 1")

    await track.eval_prop()





@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
