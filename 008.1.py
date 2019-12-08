import sys


def get_layer(image, size, layer):
    _s = size[0] * size[1]
    i = _s * layer
    j = _s * (layer + 1)
    if i >= len(image):
        return None

    return image[i:j]


def main():
    with open(sys.argv[1], "r") as f:
        image = f.readline().strip()

    layer_n = 0
    min_zero, min_layer = 25 * 6, -1
    layer = get_layer(image, (25, 6), layer_n)
    while layer is not None:
        zeros = layer.count("0")
        if zeros < min_zero:
            min_zero = zeros
            min_layer = layer_n
        layer_n += 1
        layer = get_layer(image, (25, 6), layer_n)

    layer = get_layer(image, (25, 6), min_layer)
    ones = layer.count("1")
    twos = layer.count("2")

    print(ones * twos)


main()
