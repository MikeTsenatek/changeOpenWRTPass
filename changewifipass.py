import pxssh
import getpass
import random
import smtplib
import time
DEFAULT_WORD_FILE = 'words-simpsons.txt'

def __get_words():
    words = []
    try:
        with open(DEFAULT_WORD_FILE, 'rb') as fd:
            words = [line.strip() for line in fd.readlines()]
    except (IOError, OSError):
        parser.error('%s file is not found. Abort!' % DEFAULT_WORD_FILE)
    return words

def gen_passphrase(words, num_words=5):
    passphrase = []
    for i in xrange(num_words):
        index = random.SystemRandom().randrange(len(words))
        passphrase.append(words[index])
    return "-".join(passphrase)


def sendemail(from_addr, to_addr_list,
              subject, message
              ):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
 
    server = smtplib.SMTP("localhost")
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()

words = __get_words()
password = gen_passphrase(words,4)

try:                                                            
    s = pxssh.pxssh()
    s.login ("hostname","root","pass")
    s.sendline ('uci set wireless.@wifi-iface[0].key="%s";uci commit wireless;wifi;wifi' % password)   # run a command
    s.prompt()             # match the prompt
    s.logout()
    sendemail("wifi@st-peter.stw.uni-erlangen.de",["vorstand@spacepub.de","admin@spacepub.de"],"Neues WLAN-Passwort","Ab sofort ist auf dem Wlan-Access-Point tempelderlust folgedenes Passwort gesetzt: %s\n\nDer Passwortwechsel wurde praesentiert von den Netzwerk-Alumni" % password)
except pxssh.ExceptionPxssh, e:
    print "pxssh failed on login."
    print str(e)

