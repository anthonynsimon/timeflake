
# Timeflake

Timeflake is a 128-bit, roughly-ordered, URL-safe UUID. Inspired by Twitter's Snowflake, Instagram's ID and Firebase's PushID.


## Features

- **Fast.** Roughly ordered (K-sortable), incremental timestamp in most significant bits enables faster indexing and less fragmentation on database indices (vs UUID v1/v4).
- **Efficient.** 128 bits: 48 bits for timestamp + 80 bits of cryptographically generated random numbers.
- **Safe.** With 1.2e+24 unique Timeflakes per millisecond, even if generating 50 million IDs per millisecond the chance of a collision is still 1 in a billion. Only likely to see a collision if generating 1.3e+12 (one trillion three hundred billion) IDs per millisecond.
- **Flexible.** Out of the box encodings in 128-bit unsigned int, hex, URL-safe base54 and raw bytes.


## Usage

```python
import timeflake

# Create a random Timeflake
flake = timeflake.random()
>>> Timeflake(base54='00mx79Rjxvfgr8qat2CeQDs')

# Get the base54, int, hex or bytes representation
flake.base54
>>> '00mx79Rjxvfgr8qat2CeQDs'

flake.hex
>>> '016fa936bff0997a0a3c428548fee8c9'

flake.int
>>> 1909005012028578488143182045514754249

flake.bytes
>>> b'\x01o\xa96\xbf\xf0\x99z\n<B\x85H\xfe\xe8\xc9'

# Convert to the standard library's UUID type
flake.uuid
>>> UUID('016fa936-bff0-997a-0a3c-428548fee8c9')

# Get the timestamp component
flake.timestamp
>>> 1579091935216

# Get the random component
flake.random
>>> 724773312193627487660233

# Parse an existing flake (you can also pass bytes, hex or int representations)
timeflake.parse(from_base54='0002HCZffkHWhKPVdXxs0YH')
>>> Timeflake(base54='0002HCZffkHWhKPVdXxs0YH')

# Create from a user defined timestamp or random value:
timeflake.from_values(timestamp=123, random=5)
>>> Timeflake(base54='00000001Wx2f4jQ0eTmSGKB')
```


## Components

```
int    = 1909000258500378892484423800037704
hex    = 00005e1ef88330b3047494e25453a148
base54 = 0002HCZ1ZqmGbaJ8YJXyp0j
```

The timeflake `0002HCZ1ZqmGbaJ8YJXyp0j` (base54) encodes the following:
```
# Milliseconds since unix epoch
timestamp = 1579088003

# Cryptographically generated random number
random    = 229975879412110228431176
```

The `hex` representation has a max length of 32 characters, while the `base54` will be 23 characters.

## Note on security
Since the timestamp is predictable, the search space within any given millisecond is 2^80 random numbers, which is meant to avoid collisions, not to secure information. Even so, it would be hard to guess any one Timeflake depending on the creation rate, it is not recommended to use them for security purposes, only for uniquely identifying resources.

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
