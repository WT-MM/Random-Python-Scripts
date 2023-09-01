

#Class for creating text template composed of HTML-like tags
class Template:
    def __init__(self):
        self.template = None
        self.items = []
    
    @classmethod
    def from_string(cls, string):
        template = cls()
        template.template = string
        return template
    
    def append_item(self, item):
        self.items.append(item)

    def to_string(self):
        self.template = ""
        for item in self.items:
            self.template += item.build_item()
        return self.template


#Class for creating HTML-like tags
class Item():
    def __init__(self, tag, attributes=None, content=None):
        self.tag = tag
        self.attributes = attributes
        self.content = content

    def build_item(self):
        item = f"<{self.tag}"
        if self.attributes:
            for attribute in self.attributes:
                item += f" {attribute}=\"{self.attributes[attribute]}\""
        if self.content:
            item += f">{self.content}</{self.tag}>"
        else:
            item += "/>"
        return item
    
    def add_attribute(self, attribute, value):
        self.attributes[attribute] = value

    def add_content(self, content):
        self.content = content

class EmptyLine(Item):
    def __init__(self):
        super().__init__("")
    
    def build_item(self):
        return "\n"
    
class Bold(Item):
    def __init__(self, content):
        super().__init__("b", content=content)
    
class Font(Item):
    def __init__(self, content, font=None):
        super().__init__("font", attributes={"font":font}, content=content)

    


    
