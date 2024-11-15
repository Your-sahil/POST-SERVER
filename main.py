import os
import random
import time
import requests

# Logo
logo = """
\033[1;37m⌌\033[1;31m━━━━\033[1;32m━━━━\033[1;33m━━━━\033[1;34m━━━━\033[1;35m━━━━\033[1;36m━━━━\033[1;37m━━━━\033[1;30m━━━━\033[1;31m━━━\033[1;32m━━━━\033[1;33m━━━━━\033[1;34m━━━━\033[1;35m━━\033[1;37m⌍
\033[1;38m▏ ______     ______     __  __     __     __        ▏
\033[1;39m▏/\  ___\   /\  __ \   /\ \_\ \   /\ \   /\ \       ▏
\033[1;35m▏\ \___  \  \ \  __ \  \ \  __ \  \ \ \  \ \ \____  ▏
\033[1;32m▏ \/\_____\  \ \_\ \_\  \ \_\ \_\  \ \_\  \ \_____\ ▏
\033[1;31m▏  \/_____/   \/_/\/_/   \/_/\/_/   \/_/   \/_____/ ▏
\033[1;37m⌎\033[1;31m━━━━\033[1;32m━━━━\033[1;33m━━━━\033[1;34m━━━━\033[1;35m━━━━\033[1;36m━━━━\033[1;37m━━━━\033[1;30m━━━━\033[1;31m━━━\033[1;32m━━━━\033[1;33m━━━━━\033[1;34m━━━━\033[1;35m━━\033[1;37m⌏                                              
                                             
\033[36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
\033[37m[*] OWNER      : \033[36mSAHIL 
\033[37m[*] GITHUB     : \033[33mSAHIL XD 
\033[37m[*] STATUS     : \033[32mPREMIUM
\033[37m[*] TEAM       : \033[35mONE MAN ARMY
\033[37m[*] TOOL       : \033[34mAUTO COMMENT TOOL
\033[36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

print(logo)

# Facebook Graph API post ID
post_id = input("\033[1;32mEnter post ID: ")
url = f'https://graph.facebook.com/v15.0/{post_id}/comments'

# Token file paths
token_file_paths = input("\033[33mEnter token file paths (comma-separated): ").split(',')

# Message file path
message_file_path = input("\033[34mEnter comment message file path: ")

# Delay between comments
delay_between_comments = int(input("\033[36mEnter delay between comments (in seconds): "))

# Read tokens from files
access_tokens = []
for token_file_path in token_file_paths:
    try:
        with open(token_file_path.strip(), "r") as token_file:
            tokens = [token.strip() for token in token_file if token.strip()]
            access_tokens.extend(tokens)
    except FileNotFoundError:
        print(f"\033[31mFile not found: {token_file_path.strip()}\033[0m")

# Read messages from file
try:
    with open(message_file_path, "r") as message_file:
        messages = [message.strip() for message in message_file if message.strip()]
except FileNotFoundError:
    print("\033[31mMessage file not found.\033[0m")
    exit()

# Validate tokens
def is_token_valid(token):
    try:
        response = requests.get(f'https://graph.facebook.com/me?access_token={token}')
        if response.status_code == 200:
            return True
        print(f"\033[31mInvalid Token: {token}\033[0m")
        return False
    except Exception as e:
        print(f"\033[31mError checking token validity: {str(e)}\033[0m")
        return False

valid_tokens = [token for token in access_tokens if is_token_valid(token)]

if not valid_tokens:
    print("\033[31mNo valid tokens available. Exiting...\033[0m")
    exit()

# Function to get account name
def get_account_name(token):
    try:
        response = requests.get(f'https://graph.facebook.com/me?access_token={token}')
        data = response.json()
        return data.get('name', 'Unknown Account')
    except Exception:
        return "Unknown Account"

# Function to post a comment
def post_comment(token, message):
    try:
        comment_params = {
            "access_token": token,
            "message": message
        }
        comment_response = requests.post(url, params=comment_params)

        if comment_response.status_code == 200:
            account_name = get_account_name(token)
            print(f"\033[32m[+] Comment Successful: {account_name} - {message}\033[0m")
        else:
            print(f"\033[31m[-] Failed to comment: {message}\033[0m")
    except Exception as e:
        print(f"\033[31mError while commenting: {str(e)}\033[0m")

# Comment processing
def process_comments():
    try:
        while True:
            token = random.choice(valid_tokens)
            message = random.choice(messages)
            post_comment(token, message)
            time.sleep(delay_between_comments)
    except KeyboardInterrupt:
        print("\033[31m\nProcess interrupted by user. Exiting...\033[0m")

# Start commenting
process_comments()
