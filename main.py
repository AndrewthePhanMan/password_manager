import os
from cryptography.fernet import Fernet

class PaswordManager:
    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        if os.path.exists(path):
            print(f"A key exists at '{path}'. Would you like to overwrite it?")
            print("This will make any passwords encrypted with the old key unreadable.")

            while True:
                overwrite = input("(y/n): ").strip().lower()
                
                if overwrite == 'y':
                    break
                elif overwrite == 'n':
                    print("Overwrite has been cancelled. Existing key unchanged.")
                    return
                else:
                    print("Invalid option. Please enter 'y' or 'n'.")

        self.key = Fernet.generate_key()

        with open(path, 'wb') as f:
            f.write(self.key)
        
        print(f"New key created at '{path}'.")

    def load_key(self, path):
        if not os.path.exists(path):
            while True:
                create = input(f"No key found at '{path}'. Would you like to create one there? (y/n): ").strip().lower()
                if create == 'y':
                    self.create_key(path)
                    return
                elif create == 'n':
                    print("Creation has been cancelled. No key was loaded.")
                    return
                else:
                    print("Invalid option. Please enter 'y' or 'n'.")
        
        with open(path, 'rb') as f:
            self.key = f.read()

    def create_password_file(self, path, dict=None):
        if os.path.exists(path):
            print(f"A password file exists at '{path}'. Would you like to overwrite it?")
            print("This will make any passwords in the file unreadable.")

            while True:
                overwrite = input("(y/n): ").strip().lower()
                
                if overwrite == 'y':
                    break
                elif overwrite == 'n':
                    print("Overwrite has been cancelled. Existing password file unchanged.")
                    return
                else:
                    print("Invalid option. Please enter 'y' or 'n'.")
        
        self.password_file = path
        open(path, 'w').close()

        if dict is not None:
            for site, password in dict.items():
                self.add_password(site, password)

    def load_password_file(self, path):
        if self.key is None:
            print("No key is loaded. Please create/load a key before loading a password file.")
            return

        if not os.path.exists(path):
            while True:
                create = input(f"No password file found at '{path}'. Would you like to create an empty one there? (y/n): ").strip().lower()
                if create == 'y':
                    self.create_password_file(path)
                    return
                elif create == 'n':
                    print("Creation has been cancelled. No password file was loaded.")
                    return
                else:
                    print("Invalid option. Please enter 'y' or 'n'.")
        
        self.password_file = path

        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()

    def add_password(self, site, password):
        if self.key is None:
            print("No key is loaded. Please create/load a key before loading a password file.")
            return

        self.password_dict[site] = password

        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")

    def get_password(self, site):
        if site not in self.password_dict:
            print(f"No password found for {site}.")
            return None        
        return self.password_dict[site]

def main():
    passwords = {
        "email":"12345",
        "google":"67890"
    }

    pm = PaswordManager()

    print("""What do you want to do?
    (1) Create a new key
    (2) Load an existing key
    (3) Create a new password file
    (4) Load an existing password file
    (5) Add a new password
    (6) Get a password
    (q) Quit
    """)

    done = False

    while not done:
        option = input("Enter option: ")
        if option == "1":
            path = input("Enter path: ")
            pm.create_key(path)
        elif option == "2":
            path = input("Enter path: ")
            pm.load_key(path)
        elif option == "3":
            path = input("Enter path: ")
            pm.create_password_file(path, passwords)
        elif option == "4":
            path = input("Enter path: ")
            pm.load_password_file(path)
        elif option == "5":
            site = input("Enter site: ")
            password = input("Enter password: ")
            pm.add_password(site, password)
        elif option == "6":
            site = input("Enter site: ")
            print(pm.get_password(site))
        elif option == "q":
            done = True
            print("Have a nice day!")
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()