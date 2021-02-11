from pickleshare import PickleShareDB

class my_DB:

    def __init__(self):
        self.db = PickleShareDB('my_pickleShare_DB')

    def add(self, username, name, apellido, password):
        st = True
        if username in self.db.keys():
            st = False
        else:
            self.db[username] = dict()
            self.db[username]['pass'] = password
            self.db[username]['name'] = name
            self.db[username]['apellido'] = apellido
            self.db[username] = self.db[username]
        return st

    def delete(self, username):
        if username in self.db.keys():
            del self.db[username]

    def setUser(self, username, name, apellido, password):
        self.delete(username)
        self.add(username, name, apellido, password)

    def getInfo(self, username):
        l = [self.db[username]['name'], self.db[username]['apellido']]
        return l

    def getAllUser(self):
        return self.db.keys()

    def is_register(self, username):
        return username in self.db.keys()

    def is_par_equal(self,password1, password2):
        return password1 == password2

    def is_password_equal(self, username, password):
        if self.is_register(username):
            return self.is_par_equal(password, self.db[username]['pass'])
        else:
            return self.is_register(username)