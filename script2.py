import pyshark
import threading
import subprocess
import time
from nextcloud import NextCloud
from nc_py_api import Nextcloud

def force_sync():
    try:
        subprocess.run(['C:\\Program Files\\Nextcloud\\nextcloudcmd.exe', '--sync -s'], shell=True)
        print("Sync successfully forced.")
    except Exception as e:
        print(f"Error: {e}")

def upload_to_nextcloud(server_url, username, password, file):
    try:
        nc = Nextcloud(nextcloud_url=server_url, nc_auth_user=username, nc_auth_pass=password)
        with open(file, 'rb') as data:
            byte_stream = data.read()
        nc.files.upload(file, byte_stream)
        
        print("Uploaded " + file)
        
    except Exception as e:
        print(f"Error uploading file {file}: {e}")

def capture_packets(interface, output_file, elapsed_time):
    capture = pyshark.LiveCapture(interface=interface, output_file=output_file)
    print("Capture started")
    capture.sniff(timeout=elapsed_time+1) 
    print("Capture stopped")

def start_capture(duration_sec, inputfile, interface, server_url, username, password):
    for file in inputfile:
        st = time.time()
        upload_to_nextcloud(server_url, username, password, file)
        et = time.time()
        elapsed_time = et - st
        print("this should take: "+str(elapsed_time)+"sec for file "+file)
        nc = Nextcloud(nextcloud_url=server_url, nc_auth_user=username, nc_auth_pass=password)
        nc.files.delete(file)
        
        output_file = file.split(".")[1] + interface + ".pcap"
        capture_thread = threading.Thread(target=capture_packets, args=(interface, output_file, elapsed_time))
        upload_thread = threading.Thread(target=upload_to_nextcloud, args=(server_url, username, password, file))

        capture_thread.start()
        upload_thread.start()

        upload_thread.join()
        force_sync()
        capture_thread.join()

if __name__ == "__main__":
    duration_sec = 1  # Adjust this value to capture packets for a desired duration
    interface = "Ethernet"
    inputfile = ["peter.jpg", "OboAndTheTCP.txt", "ReseauProjet1.zip", "tcp6or6tcp.mp4"]
    server_url = "https://cloud.werya.be"
    username = "Adrien"
    password = "72iHvCHahJe^$N"

    start_capture(duration_sec, inputfile, interface, server_url, username, password)
