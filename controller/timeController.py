import time

from database.db import database
from models.config import currentConfiguration
from models.models import User


async def voiceChannelEvent(member, before, after):
    """
    handles the voice channel events. responsible for allocating time to users
    :param member:
    :param before:
    :param after:
    :return:
    """
    if ((before.channel is None and after.channel is not None) or (
            before.channel is not None and after.channel is not None)):
        if member.id not in currentConfiguration.accs:
            data:User = database.getUserData(member.id, member.name)
            currentConfiguration.accs.update(
                {member.id: {"name": member, "time": data.discord_time, "temp_time": time.time_ns()}})

    if after.channel is not None:
        if after.self_mute and member.id not in currentConfiguration.muted:
            if currentConfiguration.accs[member.id]["temp_time"] != 0:
                currentConfiguration.accs[member.id]["time"] += int(
                    (time.time_ns() - currentConfiguration.accs[member.id]["temp_time"]) / 1000000000)
                database.setTime(member.id, currentConfiguration.accs[member.id]["time"])

                database.setCode(member.id)

                currentConfiguration.muted.append(member.id)

        elif not after.self_mute and member.id in currentConfiguration.muted:

            currentConfiguration.muted.remove(member.id)
            currentConfiguration.accs[member.id]["temp_time"] = time.time_ns()
    elif before.channel is not None and after.channel is None:
        if currentConfiguration.accs.get(member.id) is not None:
            if member.id not in currentConfiguration.muted:
                if currentConfiguration.accs[member.id]["temp_time"] != 0:
                    currentConfiguration.accs[member.id]["time"] += int(
                        (time.time_ns() - currentConfiguration.accs[member.id]["temp_time"]) / 1000000000)
                    database.setTime(member.id, currentConfiguration.accs[member.id]["time"])

                    database.setCode(member.id)

                    del currentConfiguration.accs[member.id]
                    if member.id in currentConfiguration.muted:
                        currentConfiguration.muted.remove(member.id)
