import pexpect
#  import re
import sys
#  import model
#  import sample
#  import encoder
#  import time
import string
#  import os

####### Irgendwas
def clean_input(s):
    return ''.join(filter(lambda x: x in set(string.printable), s))


class GPT2Text():
    def __init__(self, log):
        self.sample_ = None
        self.input = input
        self.log = log

    def get_response(self, input_str):
        sample_ = str("\n======================================== SAMPLE 1 ======================================== ").encode('utf-8')
        attempts = 0
        while attempts < 5:
            try:
                child = pexpect.spawn('python ./src/interactive_conditional_samples.py --top_k 40 --length 100 --temperature 0.9')
                child.timeout = 300
                child.expect('[*>>]')
                child.sendline(clean_input(input_str))
                child.expect('================================================================================')
                sample_ = child.before[len(input_str):]
                break
            except pexpect.exceptions.EOF:
                child.kill(0)
                attempts += 1
                print("Attempt ", attempts, "failed. Trying again.")
        return sample_.decode()

    def clean_response(self, resp):
        resp = str(resp[92:]).encode('utf-8')
        resp = resp.split('<|endoftext|>'.encode('utf-8'))[0]
        sp = resp.splitlines()
        self.log("Split len", len(sp))
        out = ""
        ctr = 1
        lp = len(sp)
        stop = False
        pref = ""
        while ctr < len(sp):
            if len(sp[0]) > 0 and ord('=') in sp[0][:min(2, len(sp[0]))] and not stop:
                stop = True
                del sp[0]
                if len(sp) < 1 or ctr == (lp-1):
                    break
                lp = len(sp)
            out += "" + sp[ctr].decode() + "\n"
            ctr += 1
            #  if len(out) > len(inp):
            #      break
        if len(out) < 4:
            return ""
        return str(pref + "\n" + out)


if __name__ == "__main__":
    with open("./bot_logs.txt", 'a+') as log:
        w = sys.stdout.write

        def wlog(data, flush=False, silent=False):
            data += "\n"
            if not silent:
                w(data)
            log.write(data)
            if flush:
                log.flush()

        bot = GPT2Text(wlog)
        print("before cleaned:")
        gpt_out = bot.get_response(sys.argv[1])
        print(gpt_out)
        print("\n\n\nafter cleaned:\n")
        print(bot.clean_response(gpt_out))
