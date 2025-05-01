class UserModel:
    def __init__(self, fpath):
        self.fpath = fpath

    def get_users(self):
        users = []
        with open(self.fpath, "r") as f:
            for line in f:
                username, age = line.split(",")
                users.append({ "username": username.strip(), "age": int(age.strip()) })
        return users