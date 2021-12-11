
<h1 align="center">
<sub>
    <!-- <img src="https://www.cloudflare.com/static/e483f0dab463205cec2642ab111e81fc/cdn-global-hero-illustration.svg" height="36"> -->
</sub>
&nbsp;
kozumikku.py
</h1>
<p align="center">
<sup>
An asynchronous library for interacting with the Kozumikku API.
</sup>
<br>
<sup>
    <a href="https://www.digitalocean.com/community/tutorials/how-to-host-a-website-using-cloudflare-and-nginx-on-ubuntu-20-04">Read the docs.</a>
</sup>
</p>

***

Key Features
-------------

- Modern Pythonic API using `async` and `await`
- Sane Error handling
- Correct authentication

Installing
-----------

**Python 3.8 or higher is required**

Installing the library without HTTP speedups:
```sh
# Linux/MacOS
python3 -m pip install -U kozumikku.py

# Windows
py -3 -m pip install -U kozumikku.py
```
Otherwise, to get the HTTP speedups, run the following command:
```sh
# Linux/MacOS
python3 -m pip install -U kozumikku.py[speedups]

# Windows
py-3 -m pip install -U kozumikku.py[speedups]
```

Examples
--------

```py
from kozumikku import KozumikkuClient


client = KozumikkuClient("API-TOKEN-HERE")
# get an api token here: https://www.kozumikku.tech/api/

# Requesting endpoints

## Say we have an endpoint in the /image/ category, and we need to
## request the /flip/ endpoint for it. We can simply run this:
image: bytes = await client.image("flip", url="image-url")

# Read the docs for more information
```



