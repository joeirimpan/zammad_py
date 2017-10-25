=================
Zammad API Client
=================


.. image:: https://img.shields.io/pypi/v/zammad_py.svg
        :target: https://pypi.python.org/pypi/zammad_py

.. image:: https://img.shields.io/travis/joeirimpan/zammad_py.svg
        :target: https://travis-ci.org/joeirimpan/zammad_py

.. image:: https://readthedocs.org/projects/zammad-py/badge/?version=latest
        :target: https://zammad-py.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/joeirimpan/zammad_py/shield.svg
     :target: https://pyup.io/repos/github/joeirimpan/zammad_py/
     :alt: Updates


Python API client for zammad

* Free software: MIT license
* Documentation: https://zammad-py.readthedocs.io.


Quickstart
----------

.. code-block:: python

    from zammad_py.api import ZammadAPI
    client = ZammadAPI(username='<USERNAME>', password='<PASSWORD>', host='<HOST>')
    print client.user.me()


User Resource
-------------

.. code-block:: python

    from zammad_py.api import ZammadAPI
    client = ZammadAPI(username='<USERNAME>', password='<PASSWORD>', host='<HOST>')

    print client.user.me()
    print client.user.all()
    print client.user.search({'firstname': 'Joe'})
    print client.user.find(3)
    print client.user.create({'firstname': 'Joe'})
    print client.user.update(3, {'firstname': 'Paul'})
    print client.user.destroy(3)


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

