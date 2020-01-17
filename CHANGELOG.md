# Changelog

## 0.3.1
- Use base62 as the canonical encoding.

## 0.3.0
- Switch to using 128-bit version of Timeflake.
- Improved API and conversion to various representations.

## 0.2.0
- When using the random method, it will now use the 32 bits available.
- Use base62 encoding for more standard alphabet.
- Speedup encoding and decoding by using lru_cache and alphabet index.

## 0.1.3
- Use int form of default epoch to avoid timezone issues with datetime

## 0.1.2
- Minor documentation adjustments

## 0.1.1
- Minor documentation adjustments

## 0.1.0
- Initial open source release