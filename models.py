class Contact:
    db = {}

    def __init__(self, id_=None, first=None, last=None, phone=None, email=None):
        self.id = id_
        self.first = first
        self.last = last
        self.phone = phone
        self.email = email

    @classmethod
    def all(cls):
        return list(cls.db.values())

    @classmethod
    def search(cls, text):
        result = []
        for c in cls.db.values():
            match_first = c.first is not None and text in c.first
            match_last = c.last is not None and text in c.last
            match_phone = c.phone is not None and text in c.phone
            match_email = c.email is not None and text in c.email
            if match_first or match_last or match_phone or match_email:
                result.append(c)
        return result