from enum import Enum

class FormatType(Enum):
    HTML = "html"
    BBCODE = "bbcode"

class Template:
    def __init__(self, format_type=FormatType.HTML):
        self.template = None
        self.items = []
        self.format_type = format_type
    
    @classmethod
    def from_string(string):
        #Figure out how to parse strings into Items
        template = Template()
        template.template = string
        
        return template
    
    def append_item(self, item):
        self.items.append(item)

    def get_items(self):
        return self.items
    
    def build_template(self):
        self.template = ""
        for item in self.items:
            self.template += item.build_item(format_type=self.format_type)

    def to_string(self):
        if(self.template == None):
            self.build_template()
        return self.template

#Superclass for all HTML-like items
class Item():
    def __init__(self, tag, attributes={}, content=[]):
        self.tag = tag
        self.attributes = attributes
        self.content = content

    def build_item(self, format_type=FormatType.HTML):
        self.__setClosers(format_type)
        item = self.open+self.tag
        if self.attributes:
            if format_type == FormatType.BBCODE:
                item+="="+self.attributes.get(self.tag)
                for attribute in self.attributes:
                    if attribute != self.tag:
                        item += f" {attribute}={self.attributes[attribute]}"
            elif format_type == FormatType.HTML:
                for attribute in self.attributes:
                    item += f" {attribute}=\"{self.attributes[attribute]}\""
        if self.content:
            item += self.close
            for content in self.content:
                item += content.build_item(format_type=format_type) if isinstance(content, Item) else content
            item += self.open+"/"+self.tag+self.close
        else:
            item += self.close+self.open+"/"+self.tag+self.close
        return item
    
    def __setClosers(self, format_type):
        if format_type == FormatType.HTML:
            self.open = "<"
            self.close = ">"
        
        elif format_type == FormatType.BBCODE:
            self.open = "["
            self.close = "]"
            
    
    def set_attribute(self, attribute, value):
        self.attributes[attribute] = value
    
    def get_attributes(self):
        return self.attributes
    
    def clear_attributes(self):
        self.attributes = {}

    def set_content(self, content):
        self.content = content
    
    def add_content(self, content):
        self.content.append(content)

    def get_content(self):
        return self.content

class TableRow(Item):
    def __init__(self, attributes={}, content=None):
        super().__init__("tr", attributes={}, content=content)

class TableItem(Item):
    def __init__(self, attributes={}, content=None):
        super().__init__("td", attributes={}, content=content)

class Size(Item):
    def __init__(self, size=None, content=None):
        super().__init__("size", attributes={"size":str(size)}, content=content)

class EmptyLine(Item):
    def __init__(self):
        super().__init__("")
    
    def build_item(self, format_type=FormatType.HTML):
        return "\n"

class URL(Item):
    def __init__(self, url=None, content=None):
        super().__init__("url", attributes={"href":url}, content=content)

    
class NewLine(Item):
    def __init__(self):
        super().__init__("br")
    
    def build_item(self, format_type=FormatType.HTML):
        super()._Item__setClosers(format_type)
        return self.open+"br"+self.close
    
class Bold(Item):
    def __init__(self, content):
        super().__init__("b", content=content)
    
class Font(Item):
    def __init__(self, font=None, content=None):
        super().__init__("font", attributes={"font":font}, content=content)
