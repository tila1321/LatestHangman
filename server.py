import socket
import random
import sys
import _thread
import time


users = {}

WORDARRAY = ['blue','black','yellow','pink','grey','green','brown','maroon','purple','gold']

connectedCount = 0
size = 0
randomWord = ""
guesses = ''
playerTurns = 7
hangIndex = 0
playerIndex = 0



def SendToAllPlayers(message):
    for user in users.values():
        if user is not None and user[1] is not None:
            user[1].send(bytes(message,'utf-8'))

def serverProgram():

    server = socket.socket()
    ip = '192.168.56.110'
    port = 0

    while port < 1024 or port > 65535:
        try:
          port = int(input("\nEnter the port of the host: "))
        except ValueError:
          pass


    server.bind((ip,port))
    server.listen(10)
    global randomWord
    randomWord = random.choice(WORDARRAY)
    print("The Word is: " +randomWord)
    while True:

        conn, address = server.accept()
        _thread.start_new_thread(Conn_Thread,(conn,address))
        print("Received connection from: " + str(address))

def executeGame(guess,username1):

    global guesses
    global randomWord
    global playerTurns
    global hangIndex

    failed = 0
    result = ""

    if guess not in randomWord:
        hangIndex = hangIndex + 1
        playerTurns -= 1
        if playerTurns == 0:
            SendToAllPlayers("Game Over...")
            sys.exit()
    elif len(guess) > 1 and guess != randomWord:
        hangIndex = hangIndex + 1
        playerTurns -= 1
        if playerTurns == 0:
            SendToAllPlayers("Game Over...")
            sys.exit()
    else:
        guesses += guess

    for char in randomWord:

        if char in guesses:
            result += char

        else:
            result += "_"
            failed += 1

    if failed == 0:
        SendToAllPlayers(str(username1) + " win! Congratulations!")
        time.sleep(0.05)
        SendToAllPlayers("Exit game..")
        time.sleep(0.05)
        sys.exit()
    else:
        SendToAllPlayers(str(hangIndex))
        time.sleep(0.05)
        SendToAllPlayers(result)
        time.sleep(0.05)
        SendToAllPlayers("Remaining:" + str(playerTurns))

    print(result)

def nextUser(index):

    k = 0
    for user in users:
        if k == index:
            users[user][1].send(b"Your Turn")
        k += 1

def Conn_Thread(conn,address):

    turn = 0
    username1 = None
    global playerIndex
    while True:

        data = conn.recv(1024)
        if not data:
            break

        strData = str(data, 'utf-8')
        if turn == 0:
            splited = strData.split('|',1)
            username1 = splited[0]
            if len(splited) > 1:
                password =  splited[1]
                turn = Old_User(username1, password, conn, address)
                print("oldUserReturn Turn: " + str(turn))

            else:
               turn = New_User(username1,conn,address)
               print(" newUser Turn: " + str(turn))
        elif turn == 1 and strData.isdigit() is True:
            global size
            size = int(strData)
            conn.send(bytes("Waiting for other players...", 'utf-8'))
            turn += 1
        elif turn == 1 :
            if len(users) == size:
                SendToAllPlayers("Game is started.First player is playing...")
                time.sleep(0.05)
                SendToAllPlayers("Total guess rights: " + str(playerTurns))
                time.sleep(0.05)
                SendToAllPlayers("0")
                nextUser(0)
            else:
                SendToAllPlayers(str(connectedCount) + " Players are connected. Please wait for total of " + str(size) + " players")
            turn += 1
        elif turn == 2:
            SendToAllPlayers(username1 + " Entered: " +strData)
            executeGame(strData,username1)
            playerIndex += 1
            if playerIndex == connectedCount:
                playerIndex = 0
            nextUser(playerIndex)
        else:
            pass

        print("from connected user: " + str(data,'utf-8'))

    conn.close()



def New_User(username, conn,address):

    Create_Login = username

    if Create_Login in users:
        conn.send(bytes("Already exists,please try another username:", 'utf-8'))
        return 0
    else:
        conn.send(bytes("New user password",'utf-8'))
        password = conn.recv(1024)
        users[Create_Login] = [str(password,'utf-8'),conn]

        global connectedCount
        connectedCount += 1
        if connectedCount == 1:
            conn.send(b'firstUser')
        else:
            conn.send(bytes("Login Successfull!", 'utf-8'))
        return 1



def Old_User(username,password,conn,address):

    login = username

    if login in users:
        if users[login][0] == password:

            users[login][1] = conn
            global connectedCount
            connectedCount += 1
            if connectedCount == 1:
                conn.send(b'firstUser')
            else:
                conn.send(bytes("Login Successfull!", 'utf-8'))
            return 1
        else:
            conn.send(bytes("User doesn't exist or wrong password!",'utf-8'))
            return 0
    else:
        conn.send(bytes("User doesn't exist or wrong password!",'utf-8'))
        return 0


if __name__ == "__main__":
    serverProgram()

