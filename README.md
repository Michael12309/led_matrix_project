# LED Matrix

This is made with a Raspberry Pi and a [Adafruit RGB LED Matrix](https://www.adafruit.com/product/2279).
It uses this submodule https://github.com/hzeller/rpi-rgb-led-matrix.git to simplify reading and writing to the LED matrix in CPython.

Result here:
![LED Matrix Final](https://github.com/Michael12309/led_matrix_project/assets/40968057/18b14a91-ef0a-4891-932d-4bc7f8140aa1)

(Updates live using the Yahoo Finance API)

# To run locally

1. clone with submodules

```bash
git clone --recurse-submodules [url]
```

2. set python venv

```bash
source environment/bin/activate
```

3. install cython

```bash
sudo apt update
sudo apt install cython3
```

4. install ledmatrix library (https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python)

```bash
cd submodules/matrix/
sudo apt-get update && sudo apt-get install python3-dev cython3 -y
make build-python
sudo make install-python
```
