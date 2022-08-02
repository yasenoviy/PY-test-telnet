import getpass as gp
import telnetlib as tl


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

print("========start program========\n")

HOST, password, enable = AAA_input()
print('\nResult:\n')
print(HOST)
print(password)
print(enable)


print('\n*Connection data entered*\n')

print('========end program=========')