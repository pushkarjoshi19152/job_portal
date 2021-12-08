import pymongo
import bcrypt
import linkedinbot
import naukribot
import getpass


# from pymongo import MongoClient
# uri = "mongodb+srv://cluster0.bvs04.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
# client = MongoClient(uri,
#                      tls=True,
#                      tlsCertificateKeyFile='X509-cert-9012256115599665255.pem')
# db = client['testDB']
# collection = db['testCol']


class connection:
    def __init__(self):

        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.client['jobportal']
        self.collection = self.db['users']
        # self.collection.insert_one({'_id': 1, 'name': 'pushkar'})

    def login(self):
        print('------------Login-----------\n')
        self.username = input('username: ')
        self.password = getpass.getpass(prompt='password: ')
        user = self.collection.find_one({'username': self.username})

        # print(user)
        if user:
            if bcrypt.checkpw(self.password.encode('utf-8'), user['password']):
                return False
            else:
                print('\n username or password is incorrect')
                return True
        else:
            print('\n username or password is incorrect')
            return True

    def signup(self):
        print('--------------Signup-----------\n')
        self.username = input('username: ')
        self.password = getpass.getpass(prompt='password: ')

        existing_user = self.collection.find_one({'username': self.username})

        if existing_user is None:
            hashpass = bcrypt.hashpw(
                self.password.encode('utf-8'), bcrypt.gensalt())
            print(hashpass)
            self.collection.insert_one(
                {'username': self.username, 'password': hashpass})
            return False
        else:
            print('\nUsername already exists!')
            return True

    def scrape(self):

        role = input('Job role: ')
        loc = input('Location: ')
        self.data_collection = self.db[self.username]
        print('Initializing Linkedin Bot ...\n')
        lbot = linkedinbot.LinkedInBot()

        print("Running Linkedin Bot....\n")

        data = lbot.run(role, loc)
        self.data_collection.insert_many(data)

        print('Initializing Naukri Bot ...\n')
        nbot = naukribot.NaukriBot()

        print("Running Naukri Bot....\n")

        data = nbot.run(role, loc)
        self.data_collection.insert_many(data)
    
