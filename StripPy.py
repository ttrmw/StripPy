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
while not registered:
    if sock.recv(4096).find("001") != -1:
        sock.send("JOIN " + channel + "\n")
        registered = True


def send_ch(msg, chan):
    sock.send("PRIVMSG " + chan + " :" + msg)
    print "PRIVMSG " + chan + " :" + msg

while 1:
    mail = sock.recv(4096)
    print mail
    if mail.find("PING") != -1:
        print "found ping, sending pong"
        sock.send("PONG " + mail.split()[1] + "\n")
    if mail.find("StripPy") != -1:
        send_ch("that's me!", channel)



x = raw_input()


