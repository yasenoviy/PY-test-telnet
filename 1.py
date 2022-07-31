import getpass as gp
import telnetlib as tl
from time import sleep
import socket


#functions start

def to_bytes(line):
    return f"{line}\n".encode("utf-8")

def AAA_input():
    AAA_status=0
    while(AAA_status==0):
        HOST = input("Enter host IP: ")
        user = input("Enter user login: ")
        password = gp.getpass()
 
        print('Data verify...')
        try:
            tn=tl.Telnet(HOST, timeout=10)
        except socket.timeout:
            print('IP incorrect or host not available')
        else:
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

def CMD_input():
    CMD_status = 0
    timer = 0
    commands = []
    print("Enter \"QUIT\"(CAPS) for complite enter commands")
    while CMD_status==0:
        cmd_temp = input("Enter commands[%(timer)d]" % {"timer": timer})
        if cmd_temp == 'QUIT':
            break
        else:
            commands.append(cmd_temp)
            timer = timer + 1
    return commands

def connect(HOST, user, password, commands):
    tn = tl.Telnet(HOST)
    tn.read_until(b"login: ")
    tn.write(to_bytes(user))
    sleep(1)
    if password:
        tn.read_until(b"Password: ")
        tn.write(to_bytes(password))
    print('========connected========')
    sleep(2)
    for i in range(len(commands)):
        tn.write(to_bytes(commands[i]))
        sleep(1)
    all_result = tn.read_very_eager().decode('utf-8')
    print(all_result)

#functions end


#main
print("========start program========\n")

HOST, user, password = AAA_input()
print('\nResult:\n')
print(HOST)
print(user)
print(password)

sleep(1)

print('\n*Connection data entered*\n')
sleep(1)

commands = CMD_input()
print('\nResult:\n')

for i in range(len(commands)):
    print(commands[i])
print('\n*commands entered*\n')

connect(HOST, user, password, commands)

print('========end program=========')

