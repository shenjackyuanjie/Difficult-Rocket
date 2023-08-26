class CallBackDescriptor:
    def __init__(self, name):
        self.callback_name = name

    def __set__(self, instance, value):
        assert getattr(instance, self.callback_name) is None, f"Attribute '{self.callback_name}' has been set."
        instance.__dict__[self.callback_name] = value

    def __get__(self, instance, owner):
        return (
            self
            if instance is None
            else instance.__dict__.get(self.callback_name)
        )