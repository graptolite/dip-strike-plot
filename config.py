MAGNETIC_CORRECTION = +0 # where positive is east

DATA_FILE = "example_data.csv"

SVG_FILE = "dipstrikes.svg"

# FOR 1:10k map with 4 figures grid references:

GRID_INTERVAL = 10 * 10**3 # interval in mm between the successive grid reference coordinates (10 m = 10000 mm for 4 figure grid references)
MAP_SCALE = 10000 # the second number of the ratio 1:<map scale> (10000 for 1:10k)

LINE_THICKNESS = 0.05 # px

FONT_SIZE = 1 # px

STRIKE_LINE_LENGTH = 5 # px

PLOT_DIPLESS_STRIKES = True # plot strikes without dips as just strike lines
