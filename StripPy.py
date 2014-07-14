import socket
import StripPy_api_functions.merriam_def as merriam
import StripPy_api_functions.google_suggest as suggest

class StrippyBot():

    def __init__(self, host, port, channel):
        self.host = host
        self.port = port
        self.channel = channel
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.on = False
        self.sock.settimeout(300)
        self.nick = "StripPy"

    def connect(self):
        self.sock.connect((self.host, self.port))

        self.sock.send("NICK " + self.nick + "\n")
        self.sock.send("USER " + self.nick + " 0 * :github.com/ttrmw")

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

                if len(definitions) == 0:
                    suggestions = suggest.google_suggest(mail)
                    self.send_channel("nothing found for '" + mail + "' did you mean:", self.channel)
                    for i in suggestions[:3]:
                        self.send_channel(" " + i, self.channel)
                else:
                    self.send_channel("defining '" + mail + "':", self.channel)
                    for i in definitions[:3]:
                        #succinct output
                        self.send_channel(" " + i, self.channel)

            if mail.find("strippy") != -1:
                if mail.lower().find(self.channel) == -1:
                    recipient = mail.split("!")[0].lstrip(":")
                    if not recipient == self.nick.lower():
                        self.send_channel("that's me!", recipient)
                else:
                    self.send_channel("that's me!", self.channel)

if __name__ == "__main__":
    bot = StrippyBot("irc.emerge-it.co.uk", 6667, "#dev")
    bot.connect()
