#----------------------------------------------------------------------

    # Class
def stringExtension(string = '', extension = '.ext'):
    if extension[0] == '.': extension = extension[1:]
    return string.split('.')[-1] == extension
#----------------------------------------------------------------------
