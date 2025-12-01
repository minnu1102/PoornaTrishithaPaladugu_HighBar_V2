class KasparroError(Exception):
    """Base exception for the Kasparro system."""
    pass

class SchemaValidationError(KasparroError):
    """Raised when input data does not match the required schema."""
    pass

class DataDriftError(KasparroError):
    """Raised when data distribution shifts significantly (Adaptivity)."""
    pass

class AgentExecutionError(KasparroError):
    """Raised when an agent fails to execute its core logic."""
    pass