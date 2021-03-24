#Unfinished and untested
from netmiko import ConnectHandler
import time

class CableChecker:
    def __init__(self):
       self.data = []
    
    def connect(self, host):
        nodeConfig = {
            "device_type": "cisco_ios",
            "host": host,
            "username": "admin",
            "password": "password",
            "secret": "password",
        }

        self.root = host
        return nodeConfig

    def compileOutput(self, node):
        command = "show ip int brief"
        with ConnectHandler(**node) as net_connect:
            output = net_connect.send_command(command).split()
        for i in output[6::7]:
            self.data.append(i)
        
    def testCable(self, node):
        testcommand = "test cable-diagnos tdr interface "
        showcommand = "show cable-diagnostics tdr interface "
        for i in self.data:
            with ConnectHandler(**node) as net_connect:
                net_connect.send_command(testcommand + i)
                time.sleep(40)
                output = net_connect.send_command(showcommand + i)
                print(output)
            
initialHost = "10.0.0.1"
#run = CableChecker()
#run.compileOutput(run.connect(root))
#run.testCablee(run.connect(root))


