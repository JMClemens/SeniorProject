from paramiko import SSHClient
from scp import SCPClient
import paramiko as pm

server = "192.250.236.104"
port = "1026"
user = "datagrabber"
password = "HcHp18&cj"

def createSSHClient(server, port, user, password):
    client = SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(pm.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client



ssh = createSSHClient(server, port, user, password)
scp = SCPClient(ssh.get_transport())


# Gets the logs from glastopf
scp.get('../jmc/glastopf/financialfirstgroup/log/glastopf.log')

# Gets the logs from kippo
scp.get('../caw/kippo/kippo/log/kippo.log')

