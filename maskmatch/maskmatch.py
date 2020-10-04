import hexchat
import re


__module_name__ = "banmatches"
__module_version__ = "1.0"
__module_author__ = "David Schultz (Examknow)"
__module_description__ = "Show users affected by a ban"

def irclower(s):
    return s.lower().replace('{', '[').replace('}', ']').replace('|', '\\').replace('^', '~')

mask2re = {'\\': '[\\\\|]', '|': '[\\\\|]', '^': '[~^]', '~': '[~^]', '[': '[[{]', ']': '[]}]', '{': '[[{]',
        '}': '[]}]', '*': '[^!@]*', '?': '[^!@]', '+': '\\+', '.': '\\.', '(': '\\(', ')': '\\)', '$': '\\$'}

def maskre(mask):
    "Transforms an IRC mask into a regex pattern"
    mask = irclower(mask)
    r = ''
    for c in mask:
        r += mask2re.get(c, c)
    try:
        return re.compile(r + '$', re.I)
    except:
        return None

def listify(items):
    if type(items) != list:
       items = list(items)
    return len(items) > 1 and ', '.join(items[:-1]) + ', and ' + items[-1] or items and items[0] or ''

def findAccMatch(account):
    matches = []
    list = hexchat.get_list("users")
    if list:
        for u in list:
            if u.account == account:
                matches.append(u.nick)
    return matches

def findMaskMatch(mask):
    matches = []
    list = hexchat.get_list("users")
    if list:
       mask = maskre(mask)
       if not mask:
           return
       matches = [u.nick for u in list if mask.match('%s!%s' % (u.nick, u.host))]
    return matches

def modechange(word, word_eol, userdata):
    matches = []
    if word[3] != '+b' and word[3] != '+q':
         return hexchat.EAT_NONE
    target = word[4]
    sender = word[0].split(':')[1].split('!')[0]
    if target.startswith('$a:'):
        for m in findAccMatch(target.split('$a:')[1]):
            matches.append(m)
    else:
        for m in findMaskMatch(target):
            matches.append(m)
    if word[3] == '+b':
        hexchat.emit_print("Channel Ban", sender, target)
    if word[3] == '+q':
        hexchat.emit_print("Channel Quiet", sender, target)
    if len(matches) > 0:
        print("%s %s matches %s (%s users)" % (word[3], target, listify(matches), len(matches)))
    return hexchat.EAT_HEXCHAT

hexchat.hook_server("MODE", modechange)
