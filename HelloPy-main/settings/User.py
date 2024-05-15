from settings import connect_db

class User:
    def __init__(self,name,email="default@mail.com"):
        self.name = name
        self.email = email
        
    
    def getName(self):
        return self.__name
    
    def save(self):
        print("save called!")
        connect_db.saveData(self.name,self.email)



def sendData():
    all_users = connect_db.fetchData()
    data = []
    print("calling the send data")
    for user in all_users:
        user = User(user[0],user[1])
        data.append(user)
    return data
