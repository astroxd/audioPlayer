import sys, time

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        log_file_name = "log_" + time.strftime("%d%m%Y-%H%M%S") + ".log"
        self.log = open(log_file_name, mode="a", encoding="utf8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
    
    def __getattr__(self, attr):     
        return getattr(self.terminal, attr)
    
    def flush(self):
        pass
