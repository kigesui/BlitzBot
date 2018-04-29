import argparse


class ArgParserException(Exception):
    pass


class ArgParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgParserException(message)
