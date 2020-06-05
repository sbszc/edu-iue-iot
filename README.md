# Comando de ingreso a influxdb
influx -username 'iot_practice' -password 'axfhewfghjbsdFCUHhsfjoirtSDFDwkdjb'

SHOW DATABASES

CREATE DATABASE testdata

USE testdata

INSERT temp,Name=data1 value=1.5

# Descargar la DB
https://s3.amazonaws.com/noaa.water-database/NOAA_data.txt

influx -username 'iot_practice' -password 'axfhewfghjbsdFCUHhsfjoirtSDFDwkdjb' -import -path=/var/lib/influxdb/NOAA_data.txt -precision=s -database=NOAA_water_database

# Mostar las mediciones:
show measurements

SELECT * FROM h2o_temperature LIMIT 5

# Mostrar series
SHOW SERIES

# Estructura de Influxdb
## Writing and exploring data
Now that we have a database, InfluxDB is ready to accept queries and writes.

First, a short primer on the datastore. Data in InfluxDB is organized by “time series”, which contain a measured value, like “cpu_load” or “temperature”. Time series have zero to many points, one for each discrete sample of the metric. Points consist of time (a timestamp), a measurement (“cpu_load”, for example), at least one key-value field (the measured value itself, e.g. “value=0.64”, or “temperature=21.2”), and zero to many key-value tags containing any metadata about the value (e.g. “host=server01”, “region=EMEA”, “dc=Frankfurt”).

Conceptually you can think of a measurement as an SQL table, where the primary index is always time. tags and fields are effectively columns in the table. tags are indexed, and fields are not. The difference is that, with InfluxDB, you can have millions of measurements, you don’t have to define schemas up-front, and null values aren’t stored.

Points are written to InfluxDB using the InfluxDB line protocol, which follows the following format:

<measurement>[,<tag-key>=<tag-value>...] <field-key>=<field-value>[,<field2-key>=<field2-value>...] [unix-nano-timestamp]


# Conceptos claves
## Database
https://docs.influxdata.com/influxdb/v1.8/concepts/glossary/#database

## Measurements
https://docs.influxdata.com/influxdb/v1.8/concepts/glossary/#measurement

## Series
https://docs.influxdata.com/influxdb/v1.8/concepts/glossary/#series

## Tag
https://docs.influxdata.com/influxdb/v1.8/concepts/glossary/#tag

## Field
https://docs.influxdata.com/influxdb/v1.8/concepts/glossary/#field

# Conexión a Grafana
http://iot-practice-influxdb:8086

https://medium.com/@ashrafur/beginning-visualization-with-grafana-and-influxdb-81701e10569d