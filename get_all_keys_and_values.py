import redis


if __name__ == "__main__":
    valkey = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

    keys = valkey.keys()

    # To cut down the number of round-trip transactions, pipeline() is used.
    with valkey.pipeline() as pipe:
        pipe.multi()
        for key in keys:
            pipe.get(key)
        values = pipe.execute()

    key_value_pairs = list(zip(keys, values))

    for key, value in key_value_pairs:
        print(f"{key} = {value}")
