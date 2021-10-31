class Professor:
    name = ""
    title = ""
    email = ""
    office = ""

    def __init__(self, name, title, email, office):
        self.name = name
        self.title = title
        self.email = email
        self.office = office

    def __str__(self):
        return self.name + " (" + self.title + "), " + self.email

    def get_classes(self):
        pass

    def strip_email(self):
        username = self.email.split("@")[0]
        return username.replace(".", "")

    def get_web_name(self):
        webname = self.name.replace("\"Top\" ", "")
        webname = webname.replace(" ", "-")
        webname = webname.lower()
        return webname
