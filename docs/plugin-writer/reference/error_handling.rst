.. _error-handling-basics:

Error Handling
--------------

Please see the :ref:`error-handling` section in the code guidelines.

Non fatal exceptions should be recorded with the
:meth:`~pulpcore.plugin.tasking.Task.append_non_fatal_error` method. These non-fatal exceptions
will be returned in a :attr:`~pulpcore.app.models.Task.non_fatal_errors` attribute on the resulting
:class:`~pulpcore.app.models.Task` object.


