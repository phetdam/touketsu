{# custom templating file for decorators.

   Changelog:

   07-05-2020

   initial creation. started with inspiration from ./class.rst.
#}

{# typical header templating #}
{{ fullname | escape | underline }}

.. currentmodule:: {{ module }}

.. autodecorator:: {{ objname }}
