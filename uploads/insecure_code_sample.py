# Example of insecure Python code with common vulnerabilities
import os

def insecure_function(user_input):
    # Insecure use of eval (injection vulnerability)
    eval(user_input)

def hardcoded_password():
    # Hardcoded password (sensitive information exposure)
    password = "easypeasy"

def sql_injection(user_input):
    # Example of SQL injection vulnerability
    query = "SELECT * FROM users WHERE username = '" + user_input + "';"
    os.system(query)

def insecure_file_operation():
    # Insecure file permissions
    os.chmod('/path/to/file', 0o777)

# Using a weak cryptographic hash function
import hashlib

def weak_hashing(data):
    return hashlib.md5(data.encode()).hexdigest()

# Potentially insecure subprocess use
def run_shell_command(cmd):
    os.system(cmd)