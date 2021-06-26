from django import template

register= template.Library()



# CUSTOM(USER DEFINED) TEMPLATE FILTER..BELOW

#  using decorators for registering custom filters...below
@register.filter(name='cut')
def cut(value,arg):
    """
    value - value of key in function of view.py file here hello world
    arg- any additional arguments
    this cuts out all values of 'arg' from the string!
    """
    return value.repalce(arg,'')
    # arg - what you are looking for here 'hello world'
    # '' - what you wanna repalce it with 'world' by cutting out hello.

# registering custom filters...below, function of command on line 10 and line 22 below is same,both are just ways to register custom filters. 
# register.filter('cut',cut)
# 'cut' - naming FILTER
# cut - calling fn
