# Hive home python data miner
Extracts Hive home data using the REST API using Python.

```hive_api_v6``` encapsulates low-level calls via the v6 REST API. ```hive_data_miner```, which provides a [FIRE](https://github.com/google/python-fire) CLI should be used as the entry point.

Note this implementation currently assumes that an attribute only exists in a single channel, therefore it is unlikely to work with multiple sensors (e.g. a Hive Thermostat + one or more Hive valves).

### Python Dependencies
- fire
- requests
