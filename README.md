# Yaw + Napari

Goal: Use a phone's built-in orientation (via the `deviceorientation` HTML API) to manipulate a Napari 3D transform

## Status

### 6/12/24

Signal comes through end to end. Using the Vispy Quaternion class did the trick.

However, something weird still seems to be happening between the Flask redis-set and the reading on the other end. I thought smoothing was going to fix things but in the end, it only helped minorly. There's still a large amount of 'jank' when I rotate my phone.

I suspect its something to do with the sample rate.

### 6/25/24

Upstream bug. POST is not guarenteed sequential. Switching to a Websocket solved the 'jank', which was actually just out-of-order orientations.

## Setup

1.  Generate the certificates (first time)

        openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

2.  Install dependencies

        poetry install

3.  Run Flask app

        poetry run python yaw/app.py

4.  Run Redis server ([installation](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/))

        redis-server

5.  Open napari

        poetry run python nap.py
