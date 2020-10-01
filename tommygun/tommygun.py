# -*- coding: UTF-8 -*-
import hexchat, time

__module_name__ = "tommygun"
__module_version__ = "1.0"
__module_author__ = "David Schultz (Examknow)"
__module_description__ = "Manage channels like a boss."

# Config settings #
keepop = True # Change this to False to deop after action if you weren't already opped
# End of config #

def opup():
	chan = hexchat.get_info("channel")
	if not chan.startswith('#'):
		print("Error opping up: Invalid channel")
		return hexchat.EAT_ALL
	hexchat.command('cs OP %s' % chan)
	time.sleep(1)
	return

def opped():
	me = hexchat.get_info("nick")
	for u in hexchat.get_list("users"):
		if u.nick == me:
			if '@' in u.prefix:
				return True
			else:
				return False

def oop(word, word_eol, userdata):
	chan = hexchat.get_info("channel")
	if not chan.startswith('#'):
		print("This command must be used in a channel window.")
		return hexchat.EAT_ALL
	if opped():
		print("You're already opped in", chan)
		return hexchat.EAT_ALL
	hexchat.command("cs OP " + chan)

def srb(word, word_eol, userdata):
	list = hexchat.get_list("users")
	chan = hexchat.get_info("channel")
	if len(word) < 2:
		print("Syntax is: srb <nick> [reason]")
		return hexchat.EAT_ALL

	target = word[1]
	reason = ''
	if len(word) > 2:
		reason = ' '.join(word)
		reason = reason.split(target + ' ')[1]

	if not chan.startswith('#'):
		print("This command must be used in a channel window.")
		return hexchat.EAT_ALL

	if list:
		for i in list:
			if i.nick == target:
				banmask = i.host
				ident = i.host.split('@')[0]
				cloak = i.host.split('@')[1]
				if ident.startswith('~'):
					banmask = '*!*@' + cloak
				if i.host.startswith('uid') or i.host.startswith('sid'):
					uid = ident.split('id')[1]
					if cloak.startswith('gateway/web/irccloud.com/'):
						banmask = '?id' + uid + '@' + '*irccloud*'
					else:
						banmask = '?id' + uid + '@' + cloak
				if cloak.startswith('gateway/shell/matrix.org/'):
					banmask = '$r:' + i.realname
				if cloak.startswith('gateway/web/cgi-irc/kiwiirc.com/'):
					banmask = '*!*@*' + cloak.split('ip.')[1]
				if cloak.startswith('gateway/web/thelounge/'):
					banmask = '*!*@*' + cloak.split('ip.')[1]
				if cloak.startswith('gateway/shell/xshellz/'):
					banmask = '*!*' + ident + '@gateway/shell/xshellz/*'
				if i.account != '':
					banmask = '$a:' + i.account
				wasop = True
				if not opped():
					opup()
					wasop = False
				if i.prefix == '@':
					hexchat.command('mode -o %s' % (target))
				if i.prefix == '+':
					hexchat.command('mode -v %s' % (target))
				hexchat.command('mode +b ' + banmask)
				if reason != '':
					hexchat.command('quote REMOVE ' + chan + ' ' + target + ' :' + reason)
				else:
					hexchat.command('quote REMOVE ' + chan + ' ' + target)
				if not keepop and not wasop:
					time.sleep(1)
					hexchat.command('mode -o ' + hexchat.get_info("nick"))
		return hexchat.EAT_ALL


def skb(word, word_eol, userdata):
	list = hexchat.get_list("users")
	chan = hexchat.get_info("channel")
	if len(word) < 2:
		print("Syntax is: skb <nick> [reason]")
		return hexchat.EAT_ALL

	target = word[1]
	reason = ''
	if len(word) > 2:
		reason = ' '.join(word)
		reason = reason.split(target + ' ')[1]

	if not chan.startswith('#'):
		print("This command must be used in a channel window.")
		return hexchat.EAT_ALL

	if list:
		for i in list:
			if i.nick == target:
				banmask = i.host
				ident = i.host.split('@')[0]
				cloak = i.host.split('@')[1]
				if ident.startswith('~'):
					banmask = '*!*@' + cloak
				if i.host.startswith('uid') or i.host.startswith('sid'):
					uid = ident.split('id')[1]
					if cloak.startswith('gateway/web/irccloud.com/'):
						banmask = '?id' + uid + '@' + '*irccloud*'
					else:
						banmask = '?id' + uid + '@' + cloak
				if cloak.startswith('gateway/shell/matrix.org/'):
					banmask = '$r:' + i.realname
				if cloak.startswith('gateway/web/cgi-irc/kiwiirc.com/'):
					banmask = '*!*@*' + cloak.split('ip.')[1]
				if cloak.startswith('gateway/web/thelounge/'):
					banmask = '*!*@*' + cloak.split('ip.')[1]
				if cloak.startswith('gateway/shell/xshellz/'):
					banmask = '*!*' + ident + '@gateway/shell/xshellz/*'
				if i.account != '':
					banmask = '$a:' + i.account
				wasop = True
				if not opped():
					opup()
					wasop = False
				if i.prefix == '@':
					hexchat.command('mode -o %s' % (target))
				if i.prefix == '+':
					hexchat.command('mode -v %s' % (target))
				hexchat.command('mode +b ' + banmask)
				if reason != '':
					hexchat.command('kick ' + target + ' ' + reason)
				else:
					hexchat.command('kick ' + target)
				if not keepop and not wasop:
					time.sleep(1)
					hexchat.command('mode -o ' + hexchat.get_info("nick"))
		return hexchat.EAT_ALL

def mute(word, word_eol, userdata):
	list = hexchat.get_list("users")
	chan = hexchat.get_info("channel")
	if len(word) < 2:
		print("Syntax is: mute <nick>")
		return hexchat.EAT_ALL

	target = word[1]

	if not chan.startswith('#'):
		print("This command must be used in a channel window.")
		return hexchat.EAT_ALL
	if list:
		for i in list:
			if i.nick == target:
				banmask = i.host
				ident = i.host.split('@')[0]
				cloak = i.host.split('@')[1]
				if ident.startswith('~'):
					banmask = '*!*@' + cloak
				if i.host.startswith('uid') or i.host.startswith('sid'):
					uid = ident.split('id')[1]
					if cloak.startswith('gateway/web/irccloud.com/'):
						banmask = '?id' + uid + '@' + '*irccloud*'
					else:
						banmask = '?id' + uid + '@' + cloak
				if cloak.startswith('gateway/shell/matrix.org/'):
					banmask = '$r:' + i.realname
				if cloak.startswith('gateway/web/cgi-irc/kiwiirc.com/'):
					banmask = '*!*@*' + cloak.split('ip.')[1]
				if cloak.startswith('gateway/web/thelounge/'):
					banmask = '*!*@*' + cloak.split('ip.')[1]
				if cloak.startswith('gateway/shell/xshellz/'):
					banmask = '*!*' + ident + '@gateway/shell/xshellz/*'
				if i.account != '':
					banmask = '$a:' + i.account
				wasop = True
				if not opped():
					opup()
					wasop = False
				if i.prefix == '@':
					hexchat.command('mode -o %s' % (target))
				if i.prefix == '+':
					hexchat.command('mode -v %s' % (target))
				hexchat.command('mode +q ' + banmask)
				if not keepop and not wasop:
					time.sleep(1)
					hexchat.command('mode -o ' + hexchat.get_info("nick"))
		return hexchat.EAT_ALL

def remove(word, word_eol, userdata):
	chan = hexchat.get_info("channel")
	if len(word) < 2:
		print("Syntax is: remove <nick> [reason]")
		return hexchat.EAT_ALL

	target = word[1]
	reason = ''
	if len(word) > 2:
		reason = ' '.join(word)
		reason = reason.split(target + ' ')[1]

	if not chan.startswith('#'):
		print("This command must be used in a channel window.")
		return hexchat.EAT_ALL
	wasop = True
	if not opped():
		opup()
		wasop = False
	if reason != '':
		hexchat.command('quote REMOVE ' + chan + ' ' + target + ' :' + reason)
	else:
		hexchat.command('quote REMOVE ' + chan + ' ' + target)
	if not keepop and not wasop:
		time.sleep(1)
		hexchat.command('mode -o ' + hexchat.get_info("nick"))
	return hexchat.EAT_ALL

hexchat.hook_command('srb', srb, help="Starts smart remove and ban.")
hexchat.hook_command('skb', skb, help="Starts smart kickban.")
hexchat.hook_command('mute', mute, help="Starts smart mute (quiet).")
hexchat.hook_command('oop', oop, help="Ops you with chanserv in the current channel, if you are not already.")
hexchat.hook_command('remove', remove, help="Removes a user from the channel with an optional reason.")
