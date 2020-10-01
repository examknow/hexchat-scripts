import hexchat
#########################################################################################################################
# How to use:                                                                                                           #
#   To add accounts to the ignore list, simply go to "Window -> Ignore List" and then input $a:<account> into the list. #
#   To ignore PMs from unidentified users, add $~a to the list of ignored users                                         #
#########################################################################################################################
__module_name__ = "accignore"
__module_version__ = "1.0"
__module_author__ = "David Schultz (Examknow)"
__module_description__ = "Ignore idiots with $a"

# Config Settings #
reportIgnores = True # Whether or not to notify when private messages or private notices are ignored. You will only be notified once every 20 minutes for each account.
ignoreChanMsgs = False # Whether or not to ignore channel messages as well as PMs
ignorePMs = True # Whether or not to ignore PMs from ignored accounts
ignoreNOTICEs = True # Whether or not to ignore NOTICEs from ignored accounts
# End of config #


reported = []

def ignores():
    ignores = []
    ignorelist = hexchat.get_list("ignore")
    if ignorelist:
        for i in ignorelist:
            if i.mask.startswith('$a:'):
                target = i.mask.split('$a:')[1]
                ignores.append(target)
    return ignores

def nick2acc(nick):
    list = hexchat.get_list("users")
    if list:
        for u in list:
            if u.nick == nick and u.account != '':
                account = u.account
                return account
    return '*'

def periodic_checks(userdata):
    # Run periodic checks
    reported.clear()
    return True

def pm(word, word_eol, userdata):
    nick = word[0].split(':')[1].split('!')[0]
    where = word[2]
    if where == hexchat.get_info("nick"):
        account = nick2acc(nick)
        if account == '*':
            if '$~a' in ignores():
                if nick in reported:
                    return hexchat.EAT_ALL
                print("Ignored PM from an unidentified user (%s)" % nick)
                reported.append(nick)
                return hexchat.EAT_ALL
            return hexchat.EAT_NONE
        else:
            if account in ignores():
                if account in reported:
                    return hexchat.EAT_ALL
                print("Ignored PM from %s ($a:%s)." % (nick, account))
                reported.append(account)
                return hexchat.EAT_ALL
    elif where.startswith('#') and ignoreChanMsgs:
        account = nick2acc(nick)
        if account in ignores():
            return hexchat.EAT_ALL
    return hexchat.EAT_NONE

def notice(word, word_eol, userdata):
    nick = word[0].split(':')[1].split('!')[0]
    where = word[2]
    if where == hexchat.get_info("nick"):
        account = nick2acc(nick)
        if account == '*':
            if '$~a' in ignores():
                if nick in reported:
                    return hexchat.EAT_ALL
                print("Ignored NOTICE from an unidentified user, %s ($~a)" % nick)
                reported.append(nick)
                return hexchat.EAT_ALL
            return hexchat.EAT_NONE
        else:
            if account in ignores():
                if account in reported:
                    return hexchat.EAT_ALL
                print("Ignored NOTICE from %s ($a:%s)." % (nick, account))
                reported.append(account)
                return hexchat.EAT_ALL
    elif where.startswith('#') and ignoreChanMsgs:
        account = nick2acc(nick)
        if account in ignores():
            return hexchat.EAT_ALL
hexchat.hook_server('PRIVMSG', pm)
hexchat.hook_server('NOTICE', notice)
perchecks = hexchat.hook_timer(1200000, periodic_checks)
