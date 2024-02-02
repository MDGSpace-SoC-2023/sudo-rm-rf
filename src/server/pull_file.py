import requests
import os

def download_file(filename, server_address, download_dir):
    url = f'http://{server_address}/{filename}'
    response = requests.get(url)
    if response.status_code == 200:
        download_path = os.path.join(download_dir, filename)
        with open(download_path, 'wb') as f:
            f.write(response.content)
        print(f"File '{filename}' pulled successfully to '{download_path}'")
    else:
        print("File not found on the server")

# if __name__ == "__main__":
#     path="C:\\Users\\Lenovo India\\OneDrive\\Desktop\\PixV repo\\sudo-rm-rf\\src\\Graphs\\"
#     filename=input("Enter the name of the file you want to pull :")
#     # filename_=path+filename
#     # filename = input("Enter the name of the file you want to pull: ")

#     # server_address = input("Enter the server address (e.g., 127.0.0.1:8000): ")
#     server_address="127.0.0.1:8000"
#     # download_dir = input("Enter the path where you want to download the file: ")
#     # download_dir="C:\Users\Lenovo India\OneDrive\Desktop\PixV repo\sudo-rm-rf\src\Graphs"
#     download_file(filename, server_address, path)