import jinja2
template = jinja2.Template('Hello {{ name }}')
print (template.render(name="Gobi"))
