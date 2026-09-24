"""Custom exceptions for customer search."""


class CustomerSearchException(Exception):
    """Base exception for customer search feature."""


class CustomerSearchValidationError(CustomerSearchException):
    """Raised when user input violates validation rules."""


class CustomerDataError(CustomerSearchException):
    """Raised when customer data files cannot be found, parsed, or validated."""
