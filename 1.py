import getpass as gp
from operator import truediv
from secrets import token_bytes
import telnetlib as tl
from time import sleep

def to_bytes(line):
    return f"{line}\n".encode("utf-8")

def AAA_input():
    AAA_status=0
    while(AAA_status==0):
        HOST = input("Enter host IP: ")
        user = input("Enter user login: ")
        password = gp.getpass()
        print('Data verify...')
        tn=tl.Telnet(HOST, timeout=10)
        tn.read_until(b"login: ")
        tn.write(to_bytes(user))
        sleep(1)
        tn.read_until(b"Password: ")
        tn.write(to_bytes(password))
        index, m, output = tn.expect([b'Login incorrect', b"Last login:"])
        if index == 0:
            print('User data incorrect')
        if index==1:
            AAA_status=1
            print('User data is correct!')


    return HOST, user, password

def connect(HOST, user, password):
    tn = tl.Telnet(HOST)
    tn.read_until(b"login: ")
    tn.write(to_bytes(user))
    sleep(1)
    if password:
        tn.read_until(b"Password: ")
        tn.write(to_bytes(password))
    print('========connected========')

print("========start program========")

HOST, user, password = AAA_input()

print('========data entered========')

connect(HOST, user, password)

print('========end program=========')
