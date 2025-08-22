from datetime import date, datetime, timedelta
import getpass as g
import hashlib
import os
import sys

# File names for storing hashed password and security question data
HASH_FILE = "HASH.txt"
SECURITY_FILE = "SECURITY.txt"

# ---------- UTILITY FUNCTIONS ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).digest()

def file_exists(filename):
    return os.path.exists(filename)

# ---------- PASSWORD FUNCTIONS ----------
def generate_password_hash():
    if file_exists(HASH_FILE):
        print("⚠️ A password already exists.")
        choice = input("Do you want to change the password? (yes/no): ").strip().lower()
        if choice != "yes":
            print("✔️ Keeping the existing password.")
            return
        else:
            print("🔄 Proceeding to change the password.")

    print("\n----------------- SET NEW ADMIN PASSWORD -----------------")
    new_pass = g.getpass("Enter New Password: ")
    confirm_pass = g.getpass("Confirm New Password: ")
    if new_pass != confirm_pass:
        print("❌ Passwords do not match. Try again.")
        return
    hashed = hash_password(new_pass)
    with open(HASH_FILE, "wb") as f:
        f.write(hashed)
    print("✅ Password set successfully.")

def load_stored_password_hash():
    if not file_exists(HASH_FILE):
        print("⚠️ No password hash found. Please generate a password first.")
        return None
    with open(HASH_FILE, "rb") as f:
        return f.read()

def change_password():
    stored_hash = load_stored_password_hash()
    if stored_hash is None:
        return
    old_password = g.getpass("Enter Old Password: ")
    if hash_password(old_password) != stored_hash:
        print("❌ Old password is incorrect.")
        return
    new_pass = g.getpass("Enter New Password: ")
    confirm_pass = g.getpass("Confirm New Password: ")
    if new_pass != confirm_pass:
        print("❌ New passwords do not match.")
        return
    with open(HASH_FILE, "wb") as f:
        f.write(hash_password(new_pass))
    print("✅ Password changed successfully.")

def authenticate():
    print("\n----------- ADMIN LOGIN -----------\n")
    stored_hash = load_stored_password_hash()
    if stored_hash is None:
        generate_password_hash()
        stored_hash = load_stored_password_hash()
    entered_password = g.getpass("Enter Password: ")
    if hash_password(entered_password) == stored_hash:
        print("✅ Access Granted.")
        return True
    else:
        print("❌ Access Denied.")
        return False

# ---------- SECURITY QUESTION FUNCTIONS ----------
def set_security_question():
    print("\n------ SET SECURITY QUESTION FOR PASSWORD RECOVERY ------")
    question = input("Enter your security question (e.g. Your pet's name?): ").strip()
    answer = g.getpass("Enter answer to security question: ").strip()
    confirm = g.getpass("Confirm answer: ").strip()
    if answer != confirm:
        print("❌ Answers do not match. Try again.")
        return
    hashed_answer = hash_password(answer)
    with open(SECURITY_FILE, "wb") as f:
        f.write(question.encode('utf-8') + b'\n' + hashed_answer)
    print("✅ Security question set successfully.\n")

def load_security_question_and_answer():
    if not file_exists(SECURITY_FILE):
        print("⚠️ Security question not set. Please set it first.")
        return None, None
    with open(SECURITY_FILE, "rb") as f:
        content = f.read().split(b'\n', 1)
        if len(content) != 2:
            print("❌ Security file is corrupted.")
            return None, None
        question = content[0].decode('utf-8')
        hashed_answer = content[1]

        return question, hashed_answer

def recover_password():
    print("\n---------- PASSWORD RECOVERY ----------")
    question, hashed_answer = load_security_question_and_answer()
    if question is None:
        return
    print(f"Security Question: {question}")
    user_answer = g.getpass("Enter answer: ").strip()
    if hash_password(user_answer) == hashed_answer:
        print("✅ Answer correct! You can now reset your password.")
        generate_password_hash()
    else:
        print("❌ Incorrect answer. Cannot reset password.")
      
      