# Python ratelimiting with Valkey

This is a simple ratelimiting example implemented in python using the open
source in-memory data store [Valkey](https://valkey.io).

Currently a monthly limit is implemented, but the script can also be adapted
for shorter intervals.

## How to use
1) Run `docker-compose up -d` to start the Valkey container.
2) Run `pip install -r requirements.txt` to install all dependencies.
3) Run `py simulate_api_call.py --token foo --endpoint bar --monthly-limit 5`
multiple times to test the ratelimiting.
4) Run `py get_all_keys_and_values.py` to get all stored keys and values.
5) Run `docker-compose down` to stop and remove the Valkey container after testing.

## How to check valkey directly
1) Run `docker exec -it valkey valkey-cli`
2) Execute a Valkey command.
    Examples:
    - `SET foo bar` to store key "foo" with value "bar".
    - `GET foo` to get the value for key "foo".
    - `EXPIRE foo 60` to let the key "foo" expire in 60 seconds.
    - `TTL foo` to see the time-to-live for key "foo" in seconds.
    - `KEYS *` to get all stored keys.
    - `FLUSHDB` to delete all stored keys.
