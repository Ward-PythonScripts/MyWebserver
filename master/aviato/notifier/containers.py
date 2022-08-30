class Recipient():
    def __init__(self,id,name,mail,preference) -> None:
        self.id = id
        self.name = name
        self.mail = mail
        self.preference = preference

class freeGame:
    def __init__(self, category, title, redditLink):
        self.cat = category
        self.title = title
        self.reddit = redditLink