
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
    <a href="">Read the docs.</a>
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
from kozumikku import KozumikkuClient, ImageEndpoint

kozu = KozumikkuClient("API-TOKEN-HERE", session=a_custom_session_if_you_want_to)

endpoint = ImageEndpoint.build("frostedglass") # custom args: ImageEndpoint.build("filter", filter="oceanic")
image = await client.image_endpoint(endpoint, url="image-url")

bytes_io_object = image.io
raw_bytes = image.raw
image_size = image.size
print(image)
```
```sh
>>> <Image format='image/png' size=64>
```



