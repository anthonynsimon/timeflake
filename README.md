# timeflake
Timeflakes are 64-bit (unsigned), roughly-ordered, URL-safe UIDS. Inspired by Twitter's Snowflake and Instagram's UUID.

It supports two creation methods: incremental sequence per shard ID, and cryptographically strong pseudo-random numbers.

Created since I wanted to have UIDs which are:
- Mostly incremental, to keep clustered indices on databases fast.
- Roughly-ordered for time based sorting.
- Random enough to be unique.
- Can fit in 64 bits (better cache usage, less space needed).
- Out of the box nice url safe representation.
- Easy to use with random generator, but can easily transition to sharded mode later if needed.

## Example

```python
import timeflake
timeflake.random()
>>> 'eihdZ7Hqa'
```

The resulting string `efqCcXufN` contains the following information:
```
uint64 = 4085399177663909
timestamp = 1578784406
shard_id = 123
sequence_number = 5541
```

## Properties

The IDs store the following in binary form (in this order):
- Time since custom epoch in seconds (32 bits).
- Logical shard ID (10 bits).
- Sequence number (22 bits).

Some nice properties of having an auto-incrementing sequence as the most significant part of the resulting ID are:
- Reduced performance impact when using clustered indices on relational databases (vs UUID v1/v4).
- The IDs are (roughly) sortable, so you can tell if one ID was created a few seconds before or after another.

The `.random()` method returns a new UUID using cryptographically strong pseudo-random numbers for the shard ID and sequence number (32 bits of randomness). You should expect a collision to occur if you're creating IDs at a rate of 77,162 within a single second using this method.

Once that is not enough, you can transition to using the '.next()' method (shard + counter instead of random), giving you 4,194,304 IDs per shard per second:

```python
from timeflake import Timeflake
timeflake = Timeflake(shard_id=7)
timeflake.next()
>>> 'eicbZeGxe'
# uint64=4090831824755682 timestamp=1578785671 shard_id=7 sequence_number=7138
```

By default they are encoded in base62 for (nice) URL-safe representation.

If you prefer to work with the unsigned 64-bit integer form, simply pass `encoding='uint64'` to the instance:

```python
from timeflake import Timeflake
timeflake = Timeflake(encoding='uint64')
timeflake.random()
>>> 4085399177663909
```

The default alphabet for base62 encoding is: `0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`.

When using the default epoch (2020-01-01), the IDs will run out at around 2156-02-07T07:28:15Z, giving you 100+ years of IDs.

## Supported versions
Right now the codebase is only tested with Python 3.7+.

## Dependencies
No dependencies other than the standard library.

## Contribute
Want to hack on the project? Any kind of contribution is welcome!
Simply follow the next steps:

- Fork the project.
- Create a new branch.
- Make your changes and write tests when practical.
- Commit your changes to the new branch.
- Send a pull request, it will be reviewed shortly.
- In case you want to add a feature, please create a new issue and briefly explain what the feature would consist of. For bugs or requests, before creating an issue please check if one has already been created for it.

## Changelog
Please see the [changelog](CHANGELOG.md) for more details.

## License
This project is licensed under the MIT license. Please read the [LICENSE](LICENSE) file for more details.