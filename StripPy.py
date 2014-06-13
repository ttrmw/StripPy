import socket

host = "irc.emerge-it.co.uk"
port = 6667
channel = "#dev"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

sock.send("NICK stripPy\n")
sock.send("USER stripPy 0 * :test\n")

sock.send("PRIVMSG nickserv :identify\n")

registered = False


def send_ch(msg, chan):
    sock.send("PRIVMSG " + chan + " :" + msg + "\r\n")
    print "PRIVMSG " + chan + " :" + msg


while not registered:
    if sock.recv(4096).find("001") != -1:
        sock.send("JOIN " + channel + "\r\n")
        registered = True

connected = True
while connected:
    try:
        mail = sock.recv(4096)
    except socket.error as ex:
        print ex.message
        break

    print mail
    if mail.find("PING") != -1:
        print "found ping, sending pong"
        sock.send("PONG " + mail.split()[1] + "\r\n")
        print "PONG " + mail.split()[1] + "\r\n"
    if mail.find("StripPy") != -1:
        send_ch("that's me!", channel)
