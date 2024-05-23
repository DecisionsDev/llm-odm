class LLMConfiguration:
    Name: str
    APIKey: str
    URL:  str
    Username: str

    def __init__(self):
        self.name = "default"
        
    def __init__(self, name, api_key, url, username):
        self.name = name
        self.api_key = api_key
        self.url = url
        self.username = username

    def load(self):
        print("Load configuration for", self.name)
