import getpass as gp
import telnetlib as tl
import time
import socket
import re

#functions start

def to_bytes(line):
    return f"{line}\n".encode("utf-8")

def AAA_input():
    AAA_status=0
    while(AAA_status==0):
        HOST = input("Enter host IP: ")
        password = gp.getpass()
        enable = input("Enter enable password: ")
 
        print('Data verify...')
        try:
            tn=tl.Telnet(HOST, timeout=10)
        except TimeoutError:
            print('IP incorrect or host not available')
        else:
            tn.read_until(b"Password: ")
            tn.write(to_bytes(password))
            index, m, output = tn.expect([b'Login incorrect', b"Last login:"])
            if index == 0:
                print('User data incorrect')
            if index==1:
                print('User data is correct!')
                
                index, m, output = tn.expect([b">", b"#"])
                if index == 0:
                    tn.write(b"enable\n")
                    tn.read_until(b"Password")
                    tn.write(to_bytes(enable))
                    index, m, output = tn.expect([b"Password", b"#"])
                    if index == 0:
                        print('!ENABLE password incorrect!')
                    else:
                        print('All data correct')
                        AAA_status=1

    return HOST, password, enable



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



def connect(HOST, password, enable, commands):
    tn = tl.Telnet(HOST)
    time.sleep(1)
    if password:
        tn.read_until(b"Password: ")
        tn.write(to_bytes(password))
    print('========connected========')

    index, m, output = tn.expect([b">", b"#"])
    if index == 0:
        tn.write(b"enable\n")
        tn.read_until(b"Password")
        tn.write(to_bytes(enable))
        tn.read_until(b"#", timeout=5)
        time.sleep(3)
    tn.read_very_eager()
    for cmd in commands:
        tn.write(to_bytes(cmd))
        result = ""

    while True:
        index, match, output = tn.expect([b"--More--", b"#"], timeout=5)
        output = output.decode("utf-8")
        output = re.sub(" +--More--| +\x08+ +\x08+", "\n", output)
        result += output
        if index in (1, -1):
            break
        tn.write(b" ")
        time.sleep(1)
        result.replace("\r\n", "\n")

        return result

#functions end


#main
print("========start program========\n")

HOST, password, enable = AAA_input()
print('\nResult:\n')
print(HOST)
print(password)
print(enable)

time.sleep(1)

print('\n*Connection data entered*\n')
time.sleep(1)

commands = CMD_input()

print('\nResult:\n')
for i in range(len(commands)):
    print(commands[i])
print('\n*commands entered*\n')

connect(HOST, password, enable, commands)

print('========end program=========')

