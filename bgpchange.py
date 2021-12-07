import paramiko
import argparse
import time

verbose = True
sleepTime = 0.5
receiveTime = 20000

def main():
	parser = argparse.ArgumentParser(description='BGP Prefix Changer')
	parser.add_argument('Host', metavar='host',type=str,help='Select a hostname')
	parser.add_argument('Port', metavar='port',type=str,help='Select a port')
	parser.add_argument('Username', metavar='u',type=str,help='Select a username')
	parser.add_argument('Password', metavar='p',type=str,help='Select a password')
	parser.add_argument('Prefix', metavar='pre',type=str,help='Select a prefix')
	parser.add_argument('Mask', metavar='m',type=str,help='Select a subnet mask')
	args = parser.parse_args()


	# Connect to Forti
	print("Connecting to Fortigate")  
	# Connect to the Fortigate using using the paramiko and SSH
	try:
	    remote_init_conn = paramiko.SSHClient()
	    remote_init_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	    remote_init_conn.connect(args.Host, port=args.Port, username=args.Username, password=args.Password, look_for_keys=False, allow_agent=False)
	except (paramiko.ssh_exception.AuthenticationException, paramiko.ssh_exception.SSHException) as ex:
	    print("[-] %s:%s - %s" % (args.Host, args.Port, ex))
	except paramiko.ssh_exception.NoValidConnectionsError as ex:
	    print("[-] %s:%s - %s" % (args.Host, args.Port, ex))
	
	remote_conn = connectToVDOM(remote_init_conn)
	print ("Connected to " + args.Host+":"+args.Port+" with username "+args.Username)

	print("Doing work...")
	tasks(remote_conn)

	print("Disconnecting...")
	disconnectFromFG(remote_conn)
	print("Disconnected")

def doCommand(remote_conn,command):
    remote_conn.send(command + "\n")
    output = remote_conn.recv(receiveTime)
    if verbose:
        print(output)

    time.sleep(sleepTime)

def connectToVDOM(remote_conn):
	try:
		remote_conn = remote_conn.invoke_shell()
		
	except KeyError as e:
			print(e)
	return(remote_conn)

def tasks(remote_conn):
	doCommand(remote_conn,"get system arp")

def disconnectFromFG(remote_conn):
    try:
        doCommand(remote_conn,"exit")
    except KeyError as e:
        print(e)

	
if __name__ == "__main__":
    main()