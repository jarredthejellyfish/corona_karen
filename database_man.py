import pandas

class Database:
    def __init__(self, filename):
        self.df = pandas.read_csv('database.csv')
        self.filename = filename
        
    def store_user(self, user):
        if self.in_database(user) == False:
            new_user_df = pandas.DataFrame({"CHAT_ID":[user.chat_id],
                                            "NAME":[user.name],
                                            "MESSAGE":[user.message]})
            self.df = self.df.append(new_user_df)
            self.df.to_csv(self.filename, index=False)

    def remove_user(self, user):
        chat_id = user.chat_id
        if self.in_database(user) == True:
            self.df.drop(self.df.loc[self.df['CHAT_ID']==user.chat_id].index, inplace=True)
        self.df.to_csv(self.filename, index=False)
            
    
    def in_database(self, user):
        if self.df.loc[self.df['CHAT_ID'] == user.chat_id].empty:
            return False
        else:
            return True

class User:
    def __init__(self, chat_id, name, message):
        self.chat_id = chat_id
        self.name = name
        self.message = message