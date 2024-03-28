import pyshark
import time
from nextcloud import NextCloud
from nc_py_api import Nextcloud
import subprocess

#avoir run:
#   pip install nextcloud-api-wrapper
#   pip install pyshark
#   pip install nc_py_api 

def start_capture(duration_sec, inputfile, interface, server_url, username, password):
    def force_sync():
        try:
            subprocess.run(['C:\\Program Files\\Nextcloud\\nextcloudcmd.exe', '--sync --silent'], shell=True)
            print("Sync successfully forced.")
        except Exception as e:
            print(f"Error: {e}")

    def upload_to_nextcloud(server_url, username, password, file):
        try:
            nc = Nextcloud(nextcloud_url=server_url, nc_auth_user=username, nc_auth_pass=password)
            with open(file, 'rb') as data:
                byte_stream = data.read()
            nc.files.upload(file, byte_stream)
            print("uploaded "+file)
        except Exception as e:
            print(f"Error uploading file "+file+": {e}")
        #all_files = [i for i in nc.files.listdir(depth=-1) if not i.is_dir]
        force_sync()

    
        
    for file in inputfile:
        st = time.time()
        upload_to_nextcloud(server_url, username, password, file)
        et = time.time()
        elapsed_time = et - st
        print("this should take: "+str(elapsed_time)+"sec for file "+file)

        
        st = time.time()
        capture = pyshark.LiveCapture(interface=interface, output_file=file.split(".")[1]+interface+".pcap")
        capture.sniff(timeout=elapsed_time+1)
        upload_to_nextcloud(server_url, username, password, file)
        et = time.time()
        elapsed_time2 = et - st
        print(elapsed_time2)
        print("this took: "+str(elapsed_time2)+"sec for file "+file)
        

if __name__ == "__main__":
    duration_sec = 1  # Adjust this value to capture packets for a desired duration
    interface="Ethernet"
    inputfile=["peter.jpg","OboAndTheTCP.txt","ReseauProjet1.zip","tcp6or6tcp.mp4"]
    server_url = "https://cloud.werya.be"
    username = "Adrien"
    password = "72iHvCHahJe^$N"

    start_capture(duration_sec, inputfile, interface, server_url, username, password)
