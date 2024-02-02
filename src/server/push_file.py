
import requests
import os

def upload_file(filename, server_address):
    url = f'http://{server_address}'
    headers = {'File-Name': os.path.basename(filename)}
    with open(filename, 'rb') as f:
        response = requests.post(url, headers=headers, data=f)
    print(response.text)

if __name__ == "__main__":
    filename_= input("Enter the name of the file you want to push: ").strip('"')
    path="C:\\Users\\Lenovo India\\OneDrive\\Desktop\\PixV repo\\sudo-rm-rf\\src\\Graphs\\"
    filename=path+filename_
    # filename = input("Enter the path of the file you want to push: ").strip('"')

    # server_address = input("Enter the server address (e.g., 127.0.0.1:8000): ")
    server_address="127.0.0.1:8000"
    upload_file(filename, server_address)