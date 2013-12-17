'''
custom filter and tags for the template engine

in order to use, incluse in the template {% ticketz_backend_extras %}

Created on Dec 8, 2013
@author: omri
@version:1.0
@copyright: Nerdeez
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
    
    def convertToNumber(varToConvert):
        '''
        will take some var and convert
        it to a number
        @param {String/Unicode/Decimal/int} - varToConvert
        @return {int/float} - a converted number
        '''
        
        try:            
        
            if (type(varToConvert) != int):
                if (type(varToConvert) == str):
                    varToConvert = float(varToConvert)
                else:
                    try:
                        varToConvert = float(varToConvert.encode())
                        
                    except:
                        varToConvert = float(varToConvert)
                        
                    finally:
                        pass
                
        except ValueError:
            print "Could not convert data to float"
            
        return varToConvert
  
    try:
        
        #result will hold the result of the multiplied numbers
        result = convertToNumber(x) * convertToNumber(y)
        result = round(result,2)
        # TODO - would need to do any localization of the result here
        
    except:
        
        #if an exception is raised, result will be set to None
        result = None
        
        #TODO - log to server
        
    finally:
        return result

