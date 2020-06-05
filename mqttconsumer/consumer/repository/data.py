from repository.connection import influx_client
from json import dumps

def save_one(time, measurement, tags, fields):
    influx_client.write_points([{
        'time': time,
        'measurement': measurement,
        'tags': tags,
        'fields': fields
    }])
