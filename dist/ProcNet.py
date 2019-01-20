from diswarm_handler import Handler
from os import urandom
from time import sleep

class _myHandler(Handler):
    def process_one(self,response):
        resp = eval(response)
        if resp[0] == 'complete':
            return (resp[0],resp[1])

class Net:
    def __init__(self,swarm,token,channel):
        self.botid = urandom(16)
        self.swarmid = swarm
        self.handler = _myHandler(channel,token,swarm,self.botid,role='client')
    def _chunk(self,codestr):
        chunks = []
        jnr = ''
        c = 0
        for i in codestr:
            jnr += i
            if c % 50 == 0 and c != 0:
                chunks.append(jnr)
                jnr = ''
            c += 1
        chunks.append(jnr)
        return chunks

    def inject_code(self,code,mode='text',params={}):
        print('Sending...')
        _name = int.from_bytes(urandom(16), byteorder="little")
        if type(code) == type(str()) and mode == 'text':
            pass
        elif type(code) == type(str()):
            with open(code,'r') as fcode:
                code = fcode.read()
        else:
            code = code.read()
        chunks = self._chunk(code)
        self.handler.request('code-inject',args=('-1',str(params),_name))
        chunknum = 0
        for i in chunks:
            self.handler.request('code-inject',args=(str(chunknum),str(i),_name))
            chunknum += 1
        self.handler.request('code-inject',args=('CHUNKCOMP',_name))
        print('Sent. Waiting for response...')
        while True:
            sleep(0.1)
            proc = self.handler.process()
            if len(proc) > 0:
                for p in proc:
                    if type(p) == tuple:
                        if p[0] == 'complete':
                            return p[1]
