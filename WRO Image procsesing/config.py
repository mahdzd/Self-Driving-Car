HSV_RANGES = {
    "green": ([45, 140, 150], [60, 180, 190]),
    "red":   ([0, 100, 80], [10, 255, 255]),           # keep lower red (unused in your case)
    "red2":  ([120, 240, 190], [180, 255, 255]),       # calibrated upper red
    "magenta": ([140, 80, 70], [160, 255, 255]),
    # "black": ([0, 0, 0], [180, 255, 50]),
}


REAL_WIDTH_CM = {
    "red": 5.0,
    "green": 5.0,
    "magenta": 5.0,
    #"black": 5.0,
}

FOCAL_LENGTH_PX =  417.56
