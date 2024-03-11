# Deckbox

A deckbox with optional divider

The box was made on a laser cutter. Because each laser cutter is different and you may be using different wood, I haven't provided the final files.

Instead I've created a script where you can adjust the different variables to suit what you need.


## The script

### Required installs

[Python 3](https://wiki.python.org/moin/BeginnersGuide/Download)

Download [this repo](https://codeload.github.com/North101/deckbox/zip/refs/heads/main) and unzip it


```bash
# setup python virtual env
python3 -m venv .venv

# activate virtual env
source .venv/bin/activate

# install required libs
python3 -m pip install -r requirements.txt
```


### Running

Activate python virtual env (if not already done)
```bash
source .venv/bin/activate
```

Generate the files with the default arguments:
```bash
python3 -m deckbox
```

To see all the arguments:
```bash
python3 -m deckbox --help
```


### Default arguments

```bash
# output directory
--output OUTPUT
# card dimensions (mm)
--dimension LENGTH WIDTH HEIGHT
# outer material thickness (mm)
--outer-thickness THICKNESS
# inner material thickness (mm)
--inner-thickness THICKNESS
# kerf (mm)
--kerf KERF
# base height as a percentage (0.0 - 1.0)
--base-percent BASE_PERCENT
# tray height as a percentage (0.0 - 1.0)
--tray-percent TRAY_PERCENT
# tab width (mm)
--tab TAB
# magnet radius (mm)
--magnet-r MAGNET_R
# divider
--divider
# icon for top or bottom
--end-icon PATH WIDTH HEIGHT SCALE
# icon for top
--top-icon PATH WIDTH HEIGHT SCALE
# icon for bottom
--bottom-icon PATH WIDTH HEIGHT SCALE
# icon for left or right side
--side-icon PATH WIDTH HEIGHT SCALE
# icon for left side
--left-icon PATH WIDTH HEIGHT SCALE
# icon for right side
--right-icon PATH WIDTH HEIGHT SCALE
# icon for front or back face
--face-icon PATH WIDTH HEIGHT SCALE
# icon for front face
--front-icon PATH WIDTH HEIGHT SCALE
# icon for back face
--back-icon PATH WIDTH HEIGHT SCALE
```


### Arguments explained

#### `--dimensions`

The length, width and height are the sizes of the cards. If you sleeve your cards then you'll want the dimensions of the sleeves.


#### `--thickness`

The thickness of the wood is important as it affects the size of everything.


#### `--kerf`

[Kerf explained](https://community.glowforge.com/t/kerf-explained-hopefully/2917)

The laser has a length and height to it which causes extra material to be removed. `kerf` is the adjustment made to compensate for that. It is also used to configure how tight the finger joints are.

The script will generate a `kerf_test.svg` to help figure out if you have the correct settings. When pushing the pieces together they should be tight.


## Materials I used

Here are the materials I used. You don't have to use the same ones but if you do you may need to make some adjustments to the arguments

Wood: [Walnut Plywood 12in x 20in (Medium Thickness)](https://shop.glowforge.com/collections/plywood/products/walnut-plywood-finished)
