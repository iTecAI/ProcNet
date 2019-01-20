from diswarm_handler import Handler
import easygui as gui
import time
from os import urandom

def check_confirm(code):
    return gui.codebox('Confirm code?','ProcNet',code)

class _handler(Handler):
    def process_one(self, response):
        resp = eval(response)
        print(resp)
        if resp[0] == 'code-inject':
            if resp[1][0] == '-1':
                return ('CIPARAM',resp[1][1],resp[1][2])
            elif resp[1][0] != 'CHUNKCOMP':
                return ('CHUNK',resp[1][1],resp[1][2])
            else:
                return ('CHUNKCOMP',resp[1][1])

        if resp[0] == 'complete':
            return ('END',resp[1])

def main(channel,token,netid):
    botid = urandom(16)
    handler = _handler(channel,token,netid,botid,role='server')
    currently_proc = None
    proclist = []
    params = None
    while True:
        time.sleep(0.1)
        proc = handler.process()
        for p in proc:
            if p[0] == 'CIPARAM' and currently_proc == None:
                print('p')
                currently_proc = p[2]
                params = p[1]
                proclist = []
            if p[0] == 'CHUNK':
                if p[2] == currently_proc:
                    print('rc')
                    proclist.append(p[1])
                    print('p-' + str(proclist))
            if p[0] == 'CHUNKCOMP' and p[1] == currently_proc:
                print('R')
                to_proc = ''.join(proclist)
                try:
                    result = eval(to_proc)
                except:
                    result = 'ERR'
                currently_proc = None
                handler.request('complete',args=(result,))
main('channel','token','netid')
