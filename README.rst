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

    from zammad_py import ZammadAPI

    # Initialize the client with the URL, username, and password
    client = ZammadAPI(url='<HOST>', username='<USERNAME>', password='<PASSWORD>')

    # Example: Access all users
    this_page = client.user.all()
    for user in this_page:
        print(user)

    # Example: Get information about the current user
    print(client.user.me())

    # Example: Create a ticket
    params = {
       "title": "Help me!",
       "group": "2nd Level",
       "customer": "david@example.com",
       "article": {
          "subject": "My subject",
          "body": "I am a message!",
          "type": "note",
          "internal": false
       }
    }
    new_ticket = client.ticket.create(params=params)



General Methods
---------------
Most resources support these methods:

.all(): Returns a paginated response with the current page number and a list of elements.

.next_page(): Returns the next page of the current pagination object.

.prev_page(): Returns the previous page of the current pagination object.

.search(params): Returns a paginated response based on the search parameters.

.find(id): Returns a single object with the specified ID.

.create(params): Creates a new object with the specified parameters.

.update(params): Updates an existing object with the specified parameters.

.destroy(id): Deletes an object with the specified ID.

Additional Resource Methods
---------------------------
User resource also has the .me() method to get information about the current user.

Ticket resource also has the .articles() method to get the articles associated with a ticket.

Link resource has methods to list, add, and delete links between objects.

TicketArticleAttachment resource has the .download() method to download a ticket attachment.

Object resource has the .execute_migrations() method to run migrations on an object.

Contributing
------------
The Zammad API Client (zammad_py) welcomes contributions.

You can contribute by reporting bugs, fixing bugs, implementing new features, writing documentation, and submitting feedback.

To get started, see the contributing section in the docs!

Please ensure that your changes include tests and updated documentation if necessary.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

