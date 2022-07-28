import getpass as gp
from operator import truediv
from secrets import token_bytes
import telnetlib as tl
from time import sleep

def AAA_input():
    AAA_status=0
    while(AAA_status!=1):
        HOST = input("Enter host IP: ")
        user = input("Enter user login: ")
        password = gp.getpass()
        print('Data verify...')
        tn=tl.Telnet(HOST)
        tn.read_until(b"login: ")
        tn.write((user))
        sleep(1)
        tn.read_until(b"Password: ")
        tn.write(password)
        if(tn.read_until(b"Last ")):
            AAA_status=1


    return HOST, user, password

def connect(HOST, user, password):
    tn = tl.Telnet(HOST)
    tn.read_until(b"login: ")
    tn.write(user)
    sleep(1)
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")

HOST, user, password = AAA_input()
connect(HOST, user, password)
