import os
import random
import time
import requests
from datetime import datetime

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
\033[37m[*] TOOL       : \033[34mAUTO COMMENT TOOL
\033[36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

print(logo)

# Input Variables
post_id = input("\033[1;32mEnter post ID: ")
url = f'https://graph.facebook.com/v15.0/{post_id}/comments'
token_file_paths = input("\033[33mEnter token file paths (comma-separated): ").split(',')
message_file_path = input("\033[34mEnter comment message file path: ")

# Delay Configuration
min_delay = 5
max_delay = 60
current_delay = min_delay

# Token and Messages
access_tokens = []
valid_tokens = []
for token_file_path in token_file_paths:
    try:
        with open(token_file_path.strip(), "r") as token_file:
            tokens = [token.strip() for token in token_file if token.strip()]
            access_tokens.extend(tokens)
    except FileNotFoundError:
        print(f"\033[31mFile not found: {token_file_path.strip()}\033[0m")

try:
    with open(message_file_path, "r") as message_file:
        messages = [message.strip() for message in message_file if message.strip()]
except FileNotFoundError:
    print("\033[31mMessage file not found.\033[0m")
    exit()

# Function to check if a token is valid
def is_token_valid(token):
    try:
        response = requests.get(f'https://graph.facebook.com/me?access_token={token}')
        return response.status_code == 200
    except Exception as e:
        print(f"\033[31mError checking token validity: {str(e)}\033[0m")
        return False

# Filter out valid tokens
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
    global current_delay
    try:
        # Modify message with dynamic variables
        modified_message = message.format(
            post_id=post_id,
            account_name=get_account_name(token),
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        comment_params = {
            "access_token": token,
            "message": modified_message
        }
        response = requests.post(url, params=comment_params)
        response_data = response.json()

        if response.status_code == 200:
            account_name = get_account_name(token)
            print(f"\033[32m[+] Comment Successful by {account_name}: {modified_message}\033[0m")
            current_delay = max(min_delay, current_delay - 1)
        else:
            error_message = response_data.get("error", {}).get("message", "Unknown Error")
            print(f"\033[31m[-] Comment Failed: {error_message}\033[0m")
            
            # Retry Mechanism
            if "rate limit" in error_message.lower() or response.status_code == 429:
                current_delay = min(max_delay, current_delay + 10)
                print(f"\033[33m[!] Increasing delay to {current_delay} seconds due to rate limit.\033[0m")
            elif "invalid token" in error_message.lower():
                print("\033[31m[-] Invalid Token. Removing it from list.\033[0m")
                valid_tokens.remove(token)
            
    except Exception as e:
        print(f"\033[31mError: {str(e)}\033[0m")

# Function to process comments
def process_comments():
    try:
        while valid_tokens:
            token = random.choice(valid_tokens)
            message = random.choice(messages)
            post_comment(token, message)
            time.sleep(current_delay)
    except KeyboardInterrupt:
        print("\033[31m\nProcess interrupted by user. Exiting...\033[0m")

# Start the comment process
process_comments()
