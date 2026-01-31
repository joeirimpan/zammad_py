class ConfigException(Exception):
    pass


class UnusedResourceError(NotImplementedError):
    """Exception raised when a method is not supported by a specific Zammad resource."""
    def __init__(self, resource_name, method_name):
        self.message = f"The method '{method_name}' is not available for the {resource_name} resource."
        super().__init__(self.message)
