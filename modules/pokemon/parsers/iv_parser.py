from . import ParserException

from data import hex2iv
from putils import Singleton

import re


class IVParser(Singleton):

    def __init__(self):
        pass

    def parse_str(self, ivs_string):
        # in: "xxx" or "xxx xxx" where x is a hex char between 0 and f
        # out: set of IV
        # raise: ParserException if ivs_string cannot be parsed
        # ivs_string = ivs_string.lower()
        iv_strings = re.findall(r'(\w+)', ivs_string)

        ret_ivs = []
        for iv_str in iv_strings:
            if len(iv_str) != 3:
                raise ParserException('"{}"({}) is not 3 chars!'.format(
                                      iv_str, len(iv_str)))

            try:
                hex_val = int(iv_str, 16)
                iv = hex2iv(hex_val)
                if iv not in ret_ivs:
                    ret_ivs.append(iv)
            except ValueError:
                raise ParserException("{} is not valid IV!".format(iv_str))

        return ret_ivs
