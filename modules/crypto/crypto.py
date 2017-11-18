from ..i_module import IModule, ExecResp
from utils.bot_config import BotConfig
from utils.bot_logger import BotLogger
from Crypto.Cipher import ARC4
import base64
import binascii
import re

from discord import Embed


class CryptoModule(IModule):

    def __init__(self):
        pass

    @staticmethod
    def encrypt(key, message):
        return None

    @staticmethod
    def decrypt(key, cipher):
        return None

    def execute(self, cmd, exec_args):
        cmd_args = cmd.split(' ')
        command = cmd_args[0]

        """
        Encryption / Decryption
        """
        if command == "enc":
            if not re.match("^enc [a-zA-Z0-9]{4} .+$", cmd):
                embed = Embed()
                embed.colour = BotConfig().get_hex("Colors", "OnError")
                embed.description = "Usage: {}enc key[4] message".format(
                                    BotConfig().get_botprefix())
                return [ExecResp(code=500, args=embed)]

            key = cmd_args[1]
            msg = ' '.join(cmd_args[2:])
            # encrypt
            rc4 = ARC4.new(key)
            cipher = rc4.encrypt(msg)
            # encode + byte to str
            b64cipher = base64.b64encode(cipher)
            b64cipher = b64cipher.decode('UTF-8')

            embed = Embed()
            embed.colour = BotConfig().get_hex("Colors", "OnSuccess")
            embed.description = b64cipher
            return [ExecResp(code=200, args=embed)]

        if command == "dec":
            if not re.match("^dec [a-zA-Z0-9]{4} .+$", cmd):
                embed = Embed()
                embed.colour = BotConfig().get_hex("Colors", "OnError")
                embed.description = "Usage: {}dec key[4] cipher".format(
                                    BotConfig().get_botprefix())
                return [ExecResp(code=500, args=embed)]

            key = cmd_args[1]
            b64cipher = ' '.join(cmd_args[2:])

            try:
                # string to byte + decode
                b64cipher = b64cipher.encode('UTF-8')
                cipher = base64.b64decode(b64cipher)

                # decrypt
                rc4 = ARC4.new(key)
                msg = rc4.decrypt(cipher)
                msg = msg.decode('UTF-8')

                embed = Embed()
                embed.colour = BotConfig().get_hex("Colors", "OnSuccess")
                embed.description = msg
                return [ExecResp(code=200, args=embed)]
            except binascii.Error:
                BotLogger().warning("Cannot decrypt: cipher wrong size")
                embed = Embed()
                embed.colour = BotConfig().get_hex("Colors", "OnError")
                embed.description = "Invalid Cipher"
                return [ExecResp(code=500, args=embed)]
            except UnicodeDecodeError:
                BotLogger().warning("Cannot decrypt: wrong key")
                embed = Embed()
                embed.colour = BotConfig().get_hex("Colors", "OnError")
                embed.description = "Invalid Key"
                return [ExecResp(code=500, args=embed)]

        return None
