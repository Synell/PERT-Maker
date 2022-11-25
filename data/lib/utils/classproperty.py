#----------------------------------------------------------------------

    # Class
class classproperty(property):
    '''This is a decorator which can be used to mark functions as class properties.

    ```py
    @classproperty
    def function(cls):
        return 'something'
    ```'''
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()
#----------------------------------------------------------------------
