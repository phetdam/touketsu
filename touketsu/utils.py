# utility functions for touketsu
#
# 07-05-2020
#
# initial creation. migrated _classdocmod and private constants over from
# touketsu.core. renamed from _utils.py to utils.py. remove _ from classdocmod.

__doc__ = "Various utilities for the ``touketsu`` package."

from textwrap import fill

# left and right formatting strings for identifier appended by _docmod_class to
# a docstring when docmod is "brief" or "fancy" (_RFMT should end with " ")
_LFMT = "**["
_RFMT = "]** "
# placeholder in warnings to be replaced with actual class name
_UNKNOWN_NAME = "[unknown_name]"
# caution statement warning about inheritance issues (to put in caution block)
_SUBCLASS_CAUTION = (":class:`" + _UNKNOWN_NAME + "` may be subclassed in only "
                     "a few cases, e.g. if its :meth:`__init__` method is not "
                     "called or if no instance attributes are added in the "
                     "subclass :meth:`__init__` method.")


def classdocmod(obj, class_type, docmod = None, docwidth = 80):
    """Modifies a class docstring.

    For the function to work properly, the docstring should be `PEP 257`__ 
    compliant. If ``docmod = "fancy"``, restructuredText will be injected into
    the docstring.

    :param obj: The class whose docstring is to be modified.
    :type obj: str
    :param class_type: Either ``"immutable"``, if the class docstring belongs to
        a class decorated by :func:`immutable`, or ``"nondynamic"`` if the
        docstring belongs to a class decorated by :func:`nondynamic`.
    :type class_type: str
    :param docmod: Specifies how to modify the docstring. As an example, suppose
        ``class_type = "immutable"``. If ``docmod = "brief"``, then the string
        ``"[Immutable] "`` will be prepended to the docstring. If
        ``docmod = "fancy"``, the formatting performed when ``docmod = "brief"``
        is performed, but a restructuredText caution block will be inserted to
        explicitly bring up the fact that a class definition decorated with
        ``"immutable"`` or ``"nondynamic"`` cannot be inherited from. If
        ``docmod`` is ``None`` or ``"identity"``, then the docstring is returned
        without any changes made.
    :type docmod: str, optional
    :param docwidth: The width of the fina
    :type docwidth: int, optional
    :rtype: None

    .. __: https://www.python.org/dev/peps/pep-0257/
    """
    _fn = classdocmod.__name__
    # if docstring is None, set to "" first
    odoc = obj.__doc__
    if odoc is None: odoc = ""
    # skip checks; supposed to be internal function
    if (docmod is None) or (docmod == "identity"): return None
    elif docmod == "brief":
        obj.__doc__ = _LFMT + class_type.title() + _RFMT + odoc
        return None
    elif docmod == "fancy":
        # split odoc by \n\n
        split_doc = odoc.split("\n\n")
        # if length of split_doc is 1, then docstring is empty or a single line.
        # else, the len(split_doc) > 1, so use the next line (element) in
        # split_doc to get the number of whitespace elements to prepend to each
        # subsequent line in the warning block.
        ws_char = " "
        ws_num = 0
        if len(split_doc) > 1:
            ws_char = split_doc[1][0]
            # ws_num may be 0 if there is no leading whitespace
            ws_num = len(split_doc[1]) - len(split_doc[1].lstrip())
        # insert caution block after first element in split_doc and wrap, with
        # all indentation equal to 3 spaces + ws_num of ws_char.
        indent = ws_char * ws_num + "   "
        split_doc.insert(1, ws_char * ws_num + ".. caution::\n\n" +
                         fill(_SUBCLASS_CAUTION.replace(_UNKNOWN_NAME,
                                                        obj.__name__),
                              width = docwidth - 3, initial_indent = indent,
                              subsequent_indent = indent))
        # join split doc with _LFMT and _RFMT and write to obj.__doc__
        obj.__doc__ = _LFMT + class_type.title() + _RFMT + \
            "\n\n".join(split_doc)
        return None
    raise ValueError("{0}: docmod must be \"brief\", \"fancy\", or "
                     "\"identity\"")

