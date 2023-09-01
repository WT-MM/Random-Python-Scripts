from Template import *



test = Template(format_type=FormatType.BBCODE)

test.append_item(EmptyLine())
test.append_item(Bold([Size(size=3,content="Hello "), NewLine(), Font(content="World!", font="Arial")]))
test.append_item(EmptyLine())

print(test.to_string())
