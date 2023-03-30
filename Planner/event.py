from datetime import datetime
from flask import abort, make_response
from database import engine
from sqlalchemy import text


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

EVENT = {
    "1000":{
        "event_title":"Show da Odium",
        "event_id": "1000",
        "event_description": "Show da melhor banda de manaus",
        "event_date": "22/03/2023",
        "user_id": "1000",
        "timestamp": get_timestamp()
    },
    "2000":{
        "event_title":"Shoegaze dos crias",
        "event_id": "2000",
        "event_description": "Show das melhores bandas de shoegaze",
        "event_date": "25/03/2023",
        "user_id": "2000",
        "timestamp": get_timestamp()
    },
    "3000":{
        "event_title":"Rodízio no faraó",
        "event_id": "3000",
        "event_description": "Rodizio nham nham",
        "event_date": "22/03/2023",
        "user_id": "3000",
        "timestamp": get_timestamp()
    }
}

def load_events_from_db():

    with engine.connect() as conn:
        result = conn.execute(text("select * from agenda_evento"))
        column_names = result.keys()
        events = []
        for row in result.all():
            events.append(dict(zip(column_names, row)))
        return events


def create_events_from_db(event_id, event_name, event_desc, event_data, event_status, user_id):

    with engine.connect() as conn:
        query = text("insert into agenda_evento values('{id}','{name}','{desc}','{data}','{status}', '{user}')".format(id = event_id, name = event_name, desc = event_desc, data = event_data, status = event_status, user = user_id))
        conn.execute(query)


def get_event_by_id(event_id):
    with engine.connect() as conn:
        query = text("select * from agenda_evento where evento_id = '{id}'".format(id=event_id))
        result = conn.execute(query)
        event_data = result.fetchone()
        if event_data:
            event = {
                'id': event_data[0],
                'name': event_data[1],
                'desc': event_data[2],
                'date': event_data[3],
                'status': event_data[4],
                'user': event_data[5]
            }
            return event
        else:
            return None


def delete_event_by_id(event_id):
    with engine.connect() as conn:
        query = text("DELETE FROM agenda_evento WHERE evento_id = '{id}'".format(id=event_id))
        result = conn.execute(query)
        if result.rowcount == 0:
            return None
        else:
            return {"Evento Deletado": event_id}

def read_all():
    return list(load_events_from_db())


def create(event):
    event_id = event.get("event_id")
    event_title = event.get("event_title", "")
    event_description = event.get("event_description", "")
    event_date = event.get("event_date", "")
    event_status = event.get("event_status", "")
    user_id = event.get("user_id", "")

    if event_id and event_id not in EVENT:
       create_events_from_db(event_id, event_title, event_description, event_date, event_status, user_id)
    else:
        abort(
            406,
            f"Event with last name {event_id} already exists",
        )

def read_one(event_id):
    event = get_event_by_id(event_id)
    if event is not None:
        return event
    else:
        abort(
            404, f"Event with ID {event_id} not found"
        )

def update(event_id, event):
    if event_id in EVENT:
        EVENT[event_id]["event_title"] = event.get("event_title", EVENT[event_id]["event_title"])
        EVENT[event_id]["event_description"] = event.get("event_description", EVENT[event_id]["event_description"])
        EVENT[event_id]["event_date"] = event.get("event_date", EVENT[event_id]["event_date"])
        EVENT[event_id]["event_status"] = event.get("event_status", EVENT[event_id]["event_status"])
        EVENT[event_id]["timestamp"] = get_timestamp()
        return EVENT[event_id]
    else:
        abort(
            404,
            f"Event ID {event_id} not found"
        )

def delete(event_id):
    event = delete_event_by_id(event_id)
    if event is not None:
        return event
    else:
        abort(
            404, f"Event with ID {event_id} not found"
        )