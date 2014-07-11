import socket
import StripPy_api_functions.merriam_def as merriam


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

        while self.connected:
            self.listen()


    def receive(self):
        return self.sock.recv(1024)

    def raw_send(self, msg):
        self.sock.send(msg + "\r\n")

    def send_channel(self, msg, recipient):
        msg = "PRIVMSG " + recipient + " :" + msg + "\r\n"
        self.raw_send(msg)
        return msg

    def listen(self):

        try:
            mail = self.receive().lower()
            print mail
        except socket.error as ex:
            return ex.message

        if mail.find("strippy on") != -1:
                self.on = True

        if mail.find("ping") != -1:
            print "found ping, sending pong"
            self.raw_send("PONG " + mail.split()[1])
            print "PONG " + mail.split()[1]

        if self.on:
            #listen for commands

            if mail.find("strippy off") != -1:
                self.on = False
                return

            if mail.find("def:") != -1:
                mail = mail.split("def:")[1].rstrip().lstrip()
                definitions = merriam.dict_lookup(mail)
                for i in range(0, 3):
                    self.send_channel(definitions[i], self.channel)

            if mail.find("strippy") != -1:
                if mail.lower().find(self.channel) == -1:
                    self.send_channel("that's me!", mail.split("!")[0].lstrip(":"))
                else:
                    self.send_channel("that's me!", self.channel)

if __name__ == "__main__":
    bot = StrippyBot("irc.emerge-it.co.uk", 6667, "#dev")
    bot.connect()
