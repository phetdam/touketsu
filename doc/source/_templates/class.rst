{# custom templating file for autosummary classes.

   Changelog:

   07-03-2020

   initial creation. really had enough with the default autosummary format.
   this file copied from default sphinx class template. commented out the
   annoying automethod init directive and method + attribute autosummaries.
#}

{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

   {% block methods -%}
   {# get rid of .. automethod:: __init__ directive #}

   {# delete entire methods autosummary as methods only includes public methods,
      i.e. methods that aren't prefixed with _ #}

   {# delete entire attributes autosummary as we don't care about attributes #}
   
   {%- endblock %}
