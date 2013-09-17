#!/usr/bin/python

import json, spur, sys, os

if len(sys.argv) == 1:
	print "Usage: "+sys.argv[0]+" [path_to_file] [ssh_username] [(optional) ssh_password]"
	exit(1)

if os.path.isfile(sys.argv[1]):
	json_data=open(sys.argv[1])
	data = json.load(json_data)
	
	for e in data:
		if len(sys.argv[2]) > 0:
			print "Connecting to "+e.upper()
			
			for t in data[e]:
				for s in data[e][t]:
					filename = e+"-"+t+"-"+s+".txt"
					print "Server: "+t+"-"+s+" with IP: "+data[e][t][s]
					
					if os.path.isfile(filename):
						os.remove(filename)

					shell = spur.SshShell(hostname=data[e][t][s], username=sys.argv[2], password=sys.argv[3], missing_host_key=spur.ssh.MissingHostKey.accept)
			
					if t == 'api':
						path = '/services/api/webapps/ROOT/WEB-INF/lib'
					elif t == 'console':
						path = '/services/console/webapps/ROOT/WEB-INF/lib'
					elif t == 'dispatcher':
						path = '/services/dispatcher/webapps/ROOT/WEB-INF/lib'
					elif t == 'km':
						path = '/services/km/webapps/ROOT/WEB-INF/lib'
					elif t == 'workers':
						path = '/services/worker/lib'
					elif t == 'monitors':
						path = '/services/monitor/lib'
					
					result = shell.run(["sudo", "find", path, "-name", "*.jar", "-ls"])
					#result2 = shell.run(["sudo", "md5sum", path+"/*.jar"])
					
					f = open(filename, "w")
					f.seek(0)
					f.write(result.output)
					#f.write(result2.output)
					f.close()
	
json_data.close()
