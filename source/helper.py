def bool_sign(boola):
    return 2*int(boola) - 1

#could be used, currently unused in anima where code is implemented


def generate_circle_offsets(radius):
        import math
        offsets = []
        radius = math.ceil(radius + math.sqrt(2)/2)   #could alternatively do math.sqrt2 / 2 and calculate nearest tile instead of truncating in both x and y
        r2 = radius * radius

        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx * dx + dy * dy <= r2:
                    offsets.append((dx, dy))

        return offsets