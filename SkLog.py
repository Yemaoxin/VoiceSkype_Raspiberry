class Sklog:
    def __init__(self):
        self.debug_level=1
        self.warning_level=2
        self.error_level=3
        self.level=0
    def setLevel(self,level):
        self.level=level

    def debug(self,msg):
        if self.level<=self.debug_level :
           print("SkLog debug: ",msg)

    def log(self,msg):
        print("SkLog log: "+msg)

    def error(self,msg):
        if(self.level<=self.error_level):
           print("SkLog error :"+msg)

    def  warning(self,msg):
        if(self.level<=self.warning_level):
            print("SkLog warning:"+msg)


