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

    size = (25, 6)
    layer_n = 0
    final_image = ["2"] * size[0] * size[1]
    layer = get_layer(image, size, layer_n)
    while layer is not None:
        for i in range(size[0] * size[1]):
            if final_image[i] == "2":
                if layer[i] != "2":
                    final_image[i] = layer[i]

        layer_n += 1
        layer = get_layer(image, size, layer_n)

    print()
    for i in range(6):
        print("".join("*" if (p == "1") else " " for p in final_image[25*i:25*(i+1)]))


main()
