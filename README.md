# EksiAPI for Python

    * Spare time project created for learning python
    * Supports Channel and Enrty search. Might improve it over time. 
    * I do not own any rights of EksiSozluk and can remove this source if requested.

## Usage

    * Be sure to check UsageExamples.py 

# Channel

```python
from EksiApi import EksiApi
import json

api = EksiApi()
print api.get_channel('gundem')
```

# Headline

```python
import eksi
print api.get_entries_by_headline('ali topu at', 1) 
```
