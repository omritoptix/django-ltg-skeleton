'''
Created on Dec 8, 2013

custom filter and tags for the template engine

in order to use, incluse in the template {% ticketz_backend_extras %}

@author: omri
'''


from django import template

register = template.Library()


'''
multiply tag will multiply two numbers.

example usage (inside a template): 

    ***
    {% multiply var1 var2 %}
    ***
    
@param1 {String/Number} - x
@param2 {String/Number} - y

@return param1 * param2

'''
        
@register.simple_tag()
def multiply(x, y, *args, **kwargs):
    # you would need to do any localization of the result here
    return x * y

