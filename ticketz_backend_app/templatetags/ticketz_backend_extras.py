'''
custom filter and tags for the template engine

in order to use, incluse in the template {% ticketz_backend_extras %}

Created on Dec 8, 2013
@author: omri
@version:1.0
@copyright: Nerdeez.com
'''


from django import template

register = template.Library()


'''
multiply tag will multiply two numbers.

example usage (inside a template): 

    ***
    {% multiply var1 var2 %}
    ***
    
@param1 {String/Number/Unicode} - x
@param2 {String/Number/Unicode} - y

@return param1 * param2

'''
        
@register.simple_tag()
def multiply(x, y, *args, **kwargs):
    

    try:
        
        if (type(x) != int):
            if (type(x) == str):
                x = float(x)
            else:
                x = float(x.encode())
                
        if (type(y) != int):
            if (type(y) == str):
                y = float(y)
            else:
                y = float(y.encode())
                
    except ValueError:
        print "Could not convert data to float"
  
    result = x * y
    result = round(result,2)
    # TODO - would need to do any localization of the result here
    return result

