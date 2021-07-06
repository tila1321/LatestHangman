import socket
import random

HANGMANPICS = ['''
    +-----+
    |     |
    |
    |
    |
    |
    ======= ''','''
    +-----+
    |     |
    |     0
    |
    |
    |
    ======= ''','''
    +-----+
    |     |
    |     0
    |     |
    |
    |
    ======= ''','''
    +-----+
    |     |
    |     0
    |    /|
    |
    |
    ======= ''','''
    +-----+
    |     |
    |     0
    |    /|\
    |
    |
    ======= ''','''
    +-----+
    |     |
    |     0
    |    /|\
    |    /
    |
 ======= ''','''
    +-----+
    |     |
    |     0
    |    /|\
    |    / \
    |
    ======= ''' ,'''
    +-----+
    |     |
    |     0
    |    /|\
    |    / \
    |     DEAD
    ======= ''']

def clientProg():

    CS = socket.socket()
    host = '192.168.56.110'
    port = 0

    print("\n[[ Available port is 1024 to 65535 ]]")
    while port < 1024 or port > 65535:
        try:
           port = int(input("\nEnter a port: "))
        except ValueError:
           pass


    CS.connect((host, port))

    print("\n")
    print("\t\t--------------------------------------------------------")
    print("\t\t（＾・ω・＾✿） Hello! Welcome to Hangman! （＾・ω・＾✿）")
    print("\t\t--------------------------------------------------------")
    print("\t\t-------------------------------------------")
    print("\t\t The goal is to guess as much as you can ")
    print("\t\t-------------------------------------------")
    print("\n")
    print("************************")
    print(" The category is COLOUR ")
    print("************************")

    login = input("\nAlready sign up to the game (y or n) ?:")

    if login == 'y' or login == 'Y':

        Username = input(" \nUsername: ")
        password = input(" Password: ")
        sendinfString = Username + "|" + password
        while Username.lower().strip() != 'bye' and password.lower().strip() != 'bye':

            CS.send(bytes(sendinfString,'utf-8'))

            data = CS.recv(1024)
            print('Received from server: ' + str(data, 'utf-8'))

            if str(data, 'utf-8') == str("Login Successfull!"):
                pass
            else:
                CS.close()
                clientProg()

    elif login == 'n' or login == 'N':
        Username = input(" Username: ")
        exist(Username,CS)
    else:
        pass

def exist(Username,CS):

    while Username.lower().strip() != 'bye':
        CS.send(bytes(Username,'utf-8'))
        data = CS.recv(1024)
        print('Received from server: ' + str(data,'utf-8'))
        if str(data,'utf-8') == str("Already exists, enter another username:"):
            Username = input(" Username: ")
            exist(Username,CS)
        else:
            Password = input(" Password: ")
            CS.send(bytes(Password, 'utf-8'))
            while Password.lower().strip() != 'bye':
                data = CS.recv(1024)
                strData = str(data, 'utf-8')

                if str(data,'utf-8') == str("firstUser"):
                    size = input("How many player wants to play?:")
                    CS.send(bytes(size,'utf-8'))
                elif str(data, 'utf-8') == str("Login Successfull!"):
                    print("Logged In!")
                    CS.send(bytes("OK", 'utf-8'))
                elif strData.isdigit():
                    print(HANGMANPICS[int(strData)])
                elif str(data,'utf-8') == str("Your Turn"):
                    guess =input("Your turn! Enter your guess:")
                    CS.send(bytes(guess,'utf-8'))
                else:
                    print('Received from server: ' + str(data, 'utf-8'))

    while Password.lower().strip() != 'bye':
        CS.send(bytes(Password,'utf-8'))
        data = CS.recv(1024)
        print('Received from server: ' + str(data, 'utf-8'))
        if str(data, 'utf-8') == str("Login Successfull!"):
            pass
        else:
           pass

    CS.close()


if __name__ == "__main__":

    clientProg()

