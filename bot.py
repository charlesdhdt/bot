import weechat
import random
import requests

SCRIPT_NAME    = "bot"
SCRIPT_AUTHOR  = "whira"
SCRIPT_VERSION = "1"
SCRIPT_LICENSE = "BSD"
SCRIPT_DESC    = "Nerf war"


def nerf_pwn(data, buffer, time, tags, displayed, highlight, prefix, message):
    buffer_name = weechat.buffer_get_string(buffer, "name")

    if not int(displayed) \
        or prefix == '--' \
        or "nerfer" not in prefix \
        or buffer_name != "lfo.#nolimit":
        return weechat.WEECHAT_RC_OK

    if "whira tu as 60secs pour '!evade `" in message:
        if "*" in message:
            res = 1
            nums = message.split()[7].split("*")
            for e in nums:
                res *= int(e)
        elif "+" in message:
            res = 0
            nums = message.split()[7].split("+")
            for e in nums:
                res += int(e)
        elif "-" in message:
            nums = message.split()[7].split("-")
            res = int(nums[0])
            nums.pop(0)
            for e in nums:
                res -= int(e)
        elif 'curl' in message:
            url = message.split()[8][:-2]
            response = requests.get(url)
            res = response.text.replace('\n','')
        else:
            res = int(message.split()[7][:-2])

        weechat.command('', '/msg -server lfo #nolimit !evade %d' % res)
        pwn_nick()

    elif "***** BIM ******" in message:
        weechat.hook_timer((5*60+1)*1000, 0, 1, "nerf_get_flechette", "")

    elif "tu as 60secs pour" in message:
        weechat.hook_timer(60*1000, 0, 1, "nerf_trigger", "")

    elif "whira:13" in message:
        weechat.hook_timer(10*60*1000, 0, 1, "nerf_score", "")
        users = [ e.split(':')[0] for e in message.split() if e != 'whira:13']
        fd = open("/tmp/score","w")
        fd.write(' '.join(users))
        fd.close()

    return weechat.WEECHAT_RC_OK


def nerf_get_flechette(data, remainingcalls):
    weechat.command('', '/msg -server lfo #nolimit !info')
    pwn_nick()
    return weechat.WEECHAT_RC_OK


def nerf_trigger(data, remainingcalls):
    weechat.command('', '/msg -server lfo #nolimit !info')
    return weechat.WEECHAT_RC_OK

def nerf_score(data, remainingcalls):
    weechat.command('', '/msg -server lfo #nolimit !score')
    return weechat.WEECHAT_RC_OK

def pwn_nick():
    fd = open("/tmp/score","r")
    users = fd.read()
    list_users = users.split()
    fd.close()

    index = random.randint(0,len(list_users)-1)
    weechat.command('', '/msg -server lfo #nolimit !nerf '+list_users[index])


if __name__ == "__main__":
    if weechat.register(SCRIPT_NAME,
        SCRIPT_AUTHOR,
        SCRIPT_VERSION,
        SCRIPT_LICENSE,
        SCRIPT_DESC,
        "",
        ""):
        weechat.hook_print("", "", "", 1, "nerf_pwn", "")
