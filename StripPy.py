import socket

<<<<<<< HEAD

class StrippyBot():

    def __init__(self, host, port, channel):
        self.host = host
        self.port = port
        self.channel = channel
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.on = False
        self.sock.settimeout(300)

    def connect(self):
        self.sock.connect((self.host, self.port))

        self.sock.send("NICK StripPy\n")
        self.sock.send("USER StripPy 0 * :github.com/ttrmw")

        self.sock.send("PRIVMSG nickserv :identify\n")

        while not self.connected:
            if self.sock.recv(4096).find("001") != -1:
                self.sock.send("JOIN " + self.channel + "\r\n")
                self.connected = True

        while not self.on:
            msg = self.receive().lower()
            print msg
            if msg.find("strippy on") != -1:
                self.on = True
                while self.connected and self.on:
                    self.listen()
                self.on = False

    def receive(self):
        return self.sock.recv(1024)

    def send(self, msg):
        self.sock.send(msg + "\r\n")

    def send_channel(self, msg, recipient):
        msg = "PRIVMSG " + recipient + " :" + msg + "\r\n"
        self.send(msg)
        return msg

    def listen(self):

        try:
            mail = self.receive().lower()
            print mail
        except socket.error as ex:
            return ex.message

        if mail.find("ping :" + self.host) != -1:
            print "found ping, sending pong"
            self.send("PONG " + mail.split()[1] + "\r\n")
            print "PONG " + mail.split()[1] + "\r\n"

        if self.on:
            #listen for commands
            if mail.find("strippy off") != -1:
                self.on = False
                return
            if mail.find("strippy") != -1:
                self.send_channel("that's me!", self.channel )

if __name__ == "__main__":
    bot = StrippyBot("irc.emerge-it.co.uk", 6667, "#dev")
    bot.connect()




=======
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
>>>>>>> 77d3b7a3e8b29d40748a0f6b1b5efa161f2211fa
