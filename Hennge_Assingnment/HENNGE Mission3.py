import json
import hmac
import hashlib
import time
import requests

# Fill in your email address and gist URL
email = "genius1392001@gmail.com"
gist_url = "https://gist.github.com/sushil1392001/1f9f4e6283981719f9a2853d243cda0a"
solution_language = "python"

# Construct the JSON string
json_data = {
    "github_url": gist_url,
    "contact_email": email,
    "solution_language": solution_language
}

# Convert the JSON data to a string
json_string = json.dumps(json_data)


def generate_totp(secret, time_step=30):
    # Get the current time in seconds
    current_time = int(time.time())
    # Calculate the counter value
    counter = current_time // time_step
    # Convert counter to bytes
    counter_bytes = counter.to_bytes(8, byteorder="big")
    # Calculate the HMAC-SHA-512 hash
    hmac_digest = hmac.new(secret.encode(), counter_bytes, hashlib.sha512).digest()
    # Get the last 4 bits of the hash to use as the offset
    offset = hmac_digest[-1] & 0x0F
    # Get the 4 bytes starting at the offset
    truncated_hash = hmac_digest[offset:offset + 4]
    # Convert the truncated hash to an integer
    otp = int.from_bytes(truncated_hash, byteorder="big") & 0x7FFFFFFF
    # Generate a 10-digit OTP
    otp = str(otp % 10 ** 10).zfill(10)
    return otp


# Construct the shared secret
shared_secret = email + "HENNGECHALLENGE003"
# Generate the TOTP password
totp_password = generate_totp(shared_secret)

# URL for the API endpoint
url = "https://api.challenge.hennge.com/challenges/003"
# HTTP Basic Authentication credentials
auth = (email, totp_password)
# Headers for the POST request
headers = {
    "Content-Type": "application/json"
}

# Make the POST request
response = requests.post(url, data=json_string, headers=headers, auth=auth)

# Print the response
print(response.status_code)
print(response.text)
