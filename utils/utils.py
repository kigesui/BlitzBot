

def get_servername(server, user_id):
    username = "{}".format(user_id)
    if server:
        member = server.get_member(user_id)
        if member:
            username = member.name
            if member.nick:
                username = member.nick
    return username
