#----------------------------------------------------------------------

    # Class
class CrossProductError(Exception):
    '''
    Exception raised for Cross Product errors.
    '''

    def __new__(cls):
        return None

    def __init__(self, message = ''):
        super().__init__(message)



class DivisionError(Exception):
    '''
    Exception raised for Division errors.
    '''

    def __new__(cls):
        return None

    def __init__(self, message = ''):
        super().__init__(message)
#----------------------------------------------------------------------
