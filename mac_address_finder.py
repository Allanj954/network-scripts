import paramiko
#mac_address_finder will recursively connect to managed devices on a subnet and search for identified mac address and its designated port.

class mac_address_finder:
    def __init__(self):
        #For production environment, do not store device information in clear text.
        self.ssh_output = None
        self.ssh_error = None
        self.client = None
        self.host= '10.0.0.1'
        self.username = 'username'
        self.password = 'password'
        self.pkey = ''
        self.port = 22

    def connect(self):
        try:
            print("Establishing SSH connection")
            self.client = paramiko.SSHClient()
            #AutoAddPolicy() function overwrites automatic Reject policy and allows connection to server without machine knowing about remote server it is trying to access. Do not use this method in production environment!
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            #Connect to the server
            if (self.password == ''):
                private_key = paramiko.RSAKey.from_private_key_file(self.pkey)
                self.client.connect(hostname=self.host, port=self.port, username=self.username, pkey=private_key, timeout=self.timeout, allow_agent=False,look_for_keys=False)
                print("Connected to the server",self.host)
            else:
                self.client.connect(hostname=self.host, port=self.port, username=self.username, password=self.password,timeout=self.timeout, allow_agent=False,look_for_keys=False)    
                print("Connected to the server",self.host)
        except paramiko.AuthenticationException:
            print("Authentication failed, please verify your credentials")
            result = False
        except paramiko.SSHException as sshException:
            print("Could not establish SSH connection: %s" % sshException)
            result = False
        except socket.timeout as e:
            print("Connection timed out")
            result = False
        except Exception,e:
            print("Exception in connecting to the server")
            print("SAYS:",e)
            result = False
            self.client.close()
        else:
            result = True
 
        return result