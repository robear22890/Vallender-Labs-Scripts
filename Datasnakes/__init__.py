class DatasnakesWarning(Warning):
    """This is the Datasnakes-Scripts main warning class.

    The Datasnakes package will use this warning to alert users about
    potential tricky code or code under development.

    >>> import warnings
    >>> from Datasnakes import DatasnakesWarning
    >>> warnings.simplefilter('ignore', OrthologsWarning)
    """

    pass


class DatasnakesDevelopmentWarning(DatasnakesWarning):
    """This is the Datasnakes developmental code warning subclass.

    This warning is for alpha or beta level code which is released as part of
    the standard releases to mark sub-modules or functions for early adopters
    to test & give feedback. Code issuing this warning is likely to change or
    removed in a subsequent release of this package. Such code should NOT be
    used for production/stable code.
    """

    pass
