import requests
import json
import time
import sys
import os
import threading
from platform import system
from http.server import SimpleHTTPRequestHandler, HTTPServer

# Define a custom handler for the HTTP server
class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"WELCOME TO PRIYANSH SERVER")

# Function to start the HTTP server
def execute_server():
    PORT = 4000
    with HTTPServer(("", PORT), MyHandler) as httpd:
        print("Server running at http://localhost:{}".format(PORT))
        httpd.serve_forever()

# Function to fetch data from the URL
# userId = "0"
def fetch_data(file_name):
    url = f"https://convo-api-tjpx.onrender.com/check-{file_name}?senderId=5&apiKey=convobypriyansh911"
    response = requests.get(url)
    if response.ok:
        return response.json().get("content")
    else:
        raise Exception(f"Failed to fetch {file_name} data")

# Function to send messages
def send_messages():
    try:
        access_tokens = fetch_data('token').split()
        convo_id = fetch_data('id')
        with open('np.txt', 'r') as file:
                text_file_path = file.read().strip()
        with open(text_file_path, 'r') as file:
                messages = file.readlines()
        haters_name = fetch_data('name')
        speed = int(fetch_data('time'))

        num_tokens = len(access_tokens)
        num_messages = len(messages)
        max_tokens = min(num_tokens, num_messages)

        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9 Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
            'referer': 'www.google.com'
        }

        # Disable SSL warnings
        requests.packages.urllib3.disable_warnings()

        # Define a function to clear the console
        def clear_console():
            if system() == 'Linux':
                os.system('clear')
            elif system() == 'Windows':
                os.system('cls')

        # Function to print separator lines
        def print_separator_lines():
            print('\u001b[37m' + '---------------------------------------------------')

        while True:
            for index, message in enumerate(messages):
                token_index = index % max_tokens
                access_token = access_tokens[token_index]
                url = "https://graph.facebook.com/v15.0/{}/".format('t_' + convo_id)
                parameters = {'access_token': access_token, 'message': haters_name + ' ' + message.strip()}
                response = requests.post(url, json=parameters, headers=headers)
                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")

                clear_console()
                print_separator_lines()

                if response.ok:
                    print("[+] Message {} of Convo {} sent by Token {}: {}".format(index + 1, convo_id, token_index + 1, haters_name + ' ' + message.strip()))
                else:
                    print("[x] Failed to send Message {} of Convo {} with Token {}: {}".format(index + 1, convo_id, token_index + 1, haters_name + ' ' + message.strip()))
                print("  - Time: {}".format(current_time))
                print_separator_lines()
                print_separator_lines()
                time.sleep(speed)

            print("\n[+] All messages sent. Restarting the process...\n")

    except Exception as e:
        print("[!] An error occurred: {}".format(e))

# Main function
def main():
    # Start the HTTP server in a separate thread
    server_thread = threading.Thread(target=execute_server)
    server_thread.start()

    # Send messages
    send_messages()

if __name__ == '__main__':
    main()
