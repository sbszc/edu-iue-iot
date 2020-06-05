from influxdb import InfluxDBClient

influx_client = InfluxDBClient(
    host = 'influxdb_mapper',
    port = 8086,
    username = 'iot_practice',
    password = 'axfhewfghjbsdFCUHhsfjoirtSDFDwkdjb',
    database = 'mapper'
)
