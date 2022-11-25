#----------------------------------------------------------------------------------------------------

    # Class
class StaticClass(type):
    '''This is a metaclass which can be used to create a Static class.
    ```py
    class MyClass(metaclass = StaticClass):
        pass
    ```'''

    def __new__(cls, *args, **kwargs) -> None:
        return None
#----------------------------------------------------------------------------------------------------
