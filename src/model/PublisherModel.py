class PublisherModel:
    def __init__(self, publisher_id, publisher_name,address:str, email:str):
        self.publisher_id = publisher_id
        self.publisher_name = publisher_name
        self.address = address
        self.email = email

    def __str__(self):
        return f"PublisherModel: {self.publisher_id}, {self.publisher_name} {self.address} {self.email}"

    def toJson(self):
        return {
            "publisher_id": self.publisher_id,
            "publisher_name": self.publisher_name,
            "address": self.address,
            "email": self.email
        }
    @staticmethod
    def fromJson(self, json):
        self.publisher_id = json["publisher_id"]
        self.publisher_name = json["publisher_name"]
        self.address = json["address"]
        self.email = json["email"]
        return self