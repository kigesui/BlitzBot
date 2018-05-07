from collections import namedtuple

IV = namedtuple("IV", "attack defense stamina")


def hex2iv(hex_val):
    if (hex_val > 0xfff) or (hex_val < 0):
        raise ValueError("{} must be between 000 and fff".format(hex_val))

    atk_val = ((hex_val & 0xf00) >> 8)
    def_val = ((hex_val & 0x0f0) >> 4)
    sta_val = hex_val & 0x00f

    return IV(attack=atk_val, defense=def_val, stamina=sta_val)
