from ..i_module import IModule, ExecResp
# from utils.bot_logger import BotLogger
from utils.bot_config import BotConfig
import re
import numpy as np
from discord import Embed

class CpModule(IModule):

    def __init__(self):
        pass

    def execute(self, cmd, exec_args):
        cmd_args = cmd.split(' ')

        command = cmd_args[0]

        if command == "cp":
            # BotLogger().debug("CP")
            if not re.match("cp [a-zA-Z]+$", cmd):
                embed = Embed()
                embed.colour = BotConfig().get_hex("Colors", "OnError")
                embed.description = "Usage: {}cp pokemon_name".format(
                                    BotConfig().get_botprefix())
                return [ExecResp(code=500, embed=embed)]
            else:
                cp_multiplier = [0.094, 0.16639787, 0.21573247, 0.25572005, 0.29024988,
                            0.3210876 , 0.34921268, 0.37523559, 0.39956728, 0.42250001,
                            0.44310755, 0.46279839, 0.48168495, 0.49985844, 0.51739395,
                            0.53435433, 0.55079269, 0.56675452, 0.58227891, 0.59740001,
                            0.61215729, 0.62656713, 0.64065295, 0.65443563, 0.667934,
                            0.68116492, 0.69414365, 0.70688421, 0.71939909, 0.7317,
                            0.73776948, 0.74378943, 0.74976104, 0.75568551, 0.76156384,
                            0.76739717, 0.7731865, 0.77893275, 0.78463697, 0.79030001]

                def compute_cp(attack, defense, stamina, cp_multiplier):
                    out = {}
                    for lvl in range(1, 31):
                        m = cp_multiplier[lvl - 1]
                        atk = (attack + 15) * m
                        defen = (defense + 15) * m
                        sta = (stamina + 15) * m
                        cp = int(max(10, np.floor(np.sqrt(
                            atk * atk * defen * sta) / 10)))
                        out[lvl] = cp
                    return out

                with open('./modules/pokemon/stats') as f:
                    data = f.read().splitlines()
                    global attack
                    global defense
                    global stamina
                    for i in data:
                        temp = i.split()
                        if re.match(temp[0], cmd_args[1], re.IGNORECASE):
                            attack = int(temp[1])
                            defense = int(temp[2])
                            stamina = int(temp[3])
                            out = compute_cp(attack, defense, stamina, cp_multiplier)
                            embed = Embed(title="Max CP for {}".format(cmd_args[1]))
                            embed.colour = BotConfig().get_hex("Colors", "OnSuccess")
                            for i in range(30, 0, -10):
                                # embed.add_field(name="LV{} to {}:".format(i, i+4),
                                #                 value="{},  {},  {},  {},  {}".format(
                                #                     out[i], out[i+1], out[i+2], out[i+3], out[i+4]),
                                #                 inline=True)
                                embed.add_field(name="LV{} to {}:".format(i, i-9),
                                                value="{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
                                                    out[i], out[i-1], out[i-2], out[i-3], out[i-4],
                                                    out[i-5], out[i-6], out[i-7], out[i-8], out[i-9]),
                                                inline=True)
                            return [ExecResp(code=200, embed=embed)]

<<<<<<< HEAD
                embed = Embed()
                embed.colour = BotConfig().get_hex("Colors", "OnError")
                embed.description = "{} is not a pokemon".format(cmd_args[1])
                return [ExecResp(code=500, embed=embed)]
=======
            cp_multiplier = [0.094, 0.16639787, 0.21573247, 0.25572005, 0.29024988,
                        0.3210876 , 0.34921268, 0.37523559, 0.39956728, 0.42250001,
                        0.44310755, 0.46279839, 0.48168495, 0.49985844, 0.51739395,
                        0.53435433, 0.55079269, 0.56675452, 0.58227891, 0.59740001,
                        0.61215729, 0.62656713, 0.64065295, 0.65443563, 0.667934,
                        0.68116492, 0.69414365, 0.70688421, 0.71939909, 0.7317,
                        0.73776948, 0.74378943, 0.74976104, 0.75568551, 0.76156384,
                        0.76739717, 0.7731865, 0.77893275, 0.78463697, 0.79030001]

            def compute_cp(attack, defense, stamina, cp_multiplier):
                out = {}
                for lvl in range(1, 31):
                    m = cp_multiplier[lvl - 1]
                    atk = (attack + 15) * m
                    defen = (defense + 15) * m
                    sta = (stamina + 15) * m
                    cp = int(max(10, np.floor(np.sqrt(
                        atk * atk * defen * sta) / 10)))
                    out[lvl] = cp
                return out

            with open(
                './modules/pokemon/stats') as f:
                data = f.read().splitlines()
                global attack
                global defense
                global stamina
                for i in data:
                    temp = i.split()
                    if temp[0].lower() == cmd_args[1].lower():
                        attack = int(temp[1])
                        defense = int(temp[2])
                        stamina = int(temp[3])
                out = compute_cp(attack, defense, stamina, cp_multiplier)

            embed = Embed(title="Max CP for {}".format(cmd_args[1]))
            embed.colour = BotConfig().get_hex("Colors", "OnSuccess")
            for i in range(30, 0, -10):
                # embed.add_field(name="LV{} to {}:".format(i, i+4),
                #                 value="{},  {},  {},  {},  {}".format(
                #                     out[i], out[i+1], out[i+2], out[i+3], out[i+4]),
                #                 inline=True)
                embed.add_field(name="LV{} to {}:".format(i, i-9),
                                value="{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
                                    out[i], out[i-1], out[i-2], out[i-3], out[i-4], 
                                    out[i-5], out[i-6], out[i-7], out[i-8], out[i-9]),
                                inline=True)
            return [ExecResp(code=200, embed=embed)]
>>>>>>> 025ea279e9316c6d0eed26481a40fe222aa3af71

        return None

    def get_cps(self):
        return {1: 123, 2: 234}
