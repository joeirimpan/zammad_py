class ConfigException(Exception):
    pass


class UnusedResourceError(NotImplementedError):
    """Exception raised when a method is not supported by a specific Zammad resource."""
    def __init__(self, resource_name, method_name):
        self.message = f"The method '{method_name}' is not available for the {resource_name} resource."
        super().__init__(self.message)


class MissingParameterError(ValueError):
    """Exception raised when a required field is missing from the parameters."""
    def __init__(self, field_name, context=None):
        self.field_name = field_name
        self.context = context
        message = f"Missing required parameter: '{field_name}'"
        if context:
            message += f" in {context}"
        super().__init__(message)


class InvalidTypeError(TypeError):
    """Exception raised when a variable is not of the expected type."""
    def __init__(self, variable_name, expected_type, actual_type):
        self.variable_name = variable_name
        self.expected_type = expected_type
        self.actual_type = actual_type
        message = (f"Variable '{variable_name}' must be of type {expected_type.__name__}, "
                   f"but got {actual_type.__name__} instead.")
        super().__init__(message)
