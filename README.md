# GNU GPL License Notice
Copyright (C) 2022  Yingbo Li

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
# Usage
1) Enter data into a csv file, whose name matches the CSV_FILE in `config.py`. This csv file must have the following header columns (additional columns may also be present, such as "site" in `example_data.csv`):

|easting|northing|strike|dip|dip direction|plane_type|
|-------|--------|------|---|-------------|----------|

2) If a magnetic correction is required, change `MAGNETIC_CORRECTION` in `config.py`.

3) Run `dip_strike.py`, which will produce an output svg file whose name is defined by `SVG_FILE` in `config.py`.

Note: currently, the accepted `plane_type`s are:
- `foliation`
- `bedding`
- `vein`
- `joint`

For `joint` and `vein`, the symbols for horizontal and vertical dips are a bit strange at the moment - however, the script should plot the dip magnitude as well, which can be used to identify planes in these specific orientations.
# Output
The scale of the output svg should be such that the dips and strikes can be directly copied and pasted into their correspondingly scaled OS map then just translated for alignment (no scaling necessary). `DOWNSCALE` (which describes the factor by which to reduce the scale) in `config.py` if a different scale is desired.

The script separates different plane types into groups, though does not separate them into different layers - this can be done manually in the svg file if desired. Colours and grouping are used to separate different dip and strike measurements at the exact same location. The dip magnitude text can be moved manually as desired by the user.

See `dipstrikes.svg` for an example output, or below for an image of what the output may look like (going from top to bottom row: bedding, foliation, joint and vein):

![Dip and Strike Symbols](./dipstrikes.png)

Note: if the svg is being opened in Inkscape, the svg elements won't necessarily be on the canvas.

# Dependencies
- matplotlib (for colours)
- numpy
- pandas
