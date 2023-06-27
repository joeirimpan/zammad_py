=====
Usage
=====

To use Zammad API Client in a project::

    from zammad_py import ZammadAPI
    # Note the Host URL should be in this format: 'https://zammad.example.org/api/v1/'
    client = ZammadAPI(url='<HOST>', username='<USERNAME>', password='<PASSWORD>')

Zammad Resources are implemented as an abstract class (Resource), meaning most objects have the same mechanisms.
Because Zammad uses pagination (https://docs.zammad.org/en/latest/api/intro.html#pagination), the pagination is very helpful.

General Methods
---------------

Most Resources support these methods.

.all()
   | Returns a paginated response with _page containing the page number and _items containing a list of elements.
   | This allows to iterate over the objects.

.. code-block:: python

    from zammad_py import ZammadAPI
    client = ZammadAPI(url='<HOST>', username='<USERNAME>', password='<PASSWORD>')
    # all return a paginated response
    this_page = client.user.all()
    # Iterate through page object
    for user in this_page:
        print(user)


.next_page()
   | Can be called from the current page (returned by .all())
   | Contains the next page object if there are any.

.. code-block:: python

    next_page = this_page.next_page()


.prev_page()
   | Can be called from the current page (pagination object)
   | Contains the previous page object if there are any.

.. code-block:: python

    prev_page = this_page.prev_page()


.search(search_string)
   | Searches the object with a Zammad search query
   | Learn more about Zammad Search queries here: https://user-docs.zammad.org/en/latest/advanced/search.html

.. code-block:: python

    from zammad_py import ZammadAPI
    client = ZammadAPI(url='<HOST>', username='<USERNAME>', password='<PASSWORD>')
    client.ticket.search('Search Content')


.find(id)
   | Displays a Resource if you know the id. (Returns a dict)

.. code-block:: python

    from zammad_py import ZammadAPI
    client = ZammadAPI(url='<HOST>', username='<USERNAME>', password='<PASSWORD>')
    client.ticket.find(<TICKETID>)


.create(params)
   | Creates a new Resource.
   | You can find the required structure for the params in the Zammad API Documentation.

.. code-block:: python

    from zammad_py import ZammadAPI
    client = ZammadAPI(url='<HOST>', username='<USERNAME>', password='<PASSWORD>')
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


.update(params)
   | Updates a resource.
   | You can find the required structure for the params in the Zammad API Documentation, or use a dict provided by the .find(id) functionaliy.

.. code-block:: python

    from zammad_py import ZammadAPI
    client = ZammadAPI(url='<HOST>', username='<USERNAME>', password='<PASSWORD>')
    org = client.organization.find(<ID>)
    org['name'] = 'NewCompanyName Ltd.'
    client.organization.update(id=org['id'],params=org)

.destroy(id)
   | Deletes a Resource.
   | For some resources, you need special privileges. Refer to the Zammad API Documentation.

.. code-block:: python

    from zammad_py import ZammadAPI
    client = ZammadAPI(url='<HOST>', username='<USERNAME>', password='<PASSWORD>')
    client.organization.destroy(<ID>)


Available Resources
    user
    organization
    group
    ticket
    link
    ticketarticle
    ticketarticleplain
    ticketpriority
    ticketstate
    object
    taglist

User Resource
-------------

The :class:`~zammad_py.api.User` resource also has the :meth:`~zammad_py.api.User.me()` method to get information about the current user.

.. code-block:: python

    from zammad_py import ZammadAPI
    client = ZammadAPI(url='<HOST>', username='<USERNAME>', password='<PASSWORD>')
    print(client.user.me())


Ticket Resource
---------------

The :class:`~zammad_py.api.Ticket` resource also has the :meth:`~zammad_py.api.Ticket.articles()` method to get the articles associated to the ticket.

.. code-block:: python

    from zammad_py import ZammadAPI
    client = ZammadAPI(url='<HOST>', username='<USERNAME>', password='<PASSWORD>')
    print(client.ticket.find(<ID>))
    ticketarticles = client.ticket.articles
    print(ticketarticles)


Further, it has the :meth:`~zammad_py.api.Ticket.merge()` method, that allows to merge two tickets. (This is not documented in the Zammad API Documentation)
The method requires the Ticket id of the Child (The ticket you want to merge into the parent) and the Ticket Number of the Parent Ticket. (The ticket you want to contain the articles of the child after merging.)

Important: If you want to use the merge functionality, you need to use password, not http_token for your authentication.

.. code-block:: python

    from zammad_py import ZammadAPI
    client = ZammadAPI(url='<HOST>', username='<USERNAME>', password='<PASSWORD>')
    client.ticket.merge(id=<ID>,number=<NUMBER>)


Link Resource
-------------

The :class:`~zammad_py.api.Link` resource also has methods to list, add and delete Links between objects.

:meth:`zammad_py.api.Link.get`
   | This returns all links associated with the ticket ID provided

:meth:`zammad_py.api.Link.add`
   | Create a Link between two objects. (Currently, and by default Tickets)

:meth:`zammad_py.api.Link.remove`
   | Remove a Link between two objects. (Currently, and by default Tickets)

.. code-block:: python

    from zammad_py import ZammadAPI
    client = ZammadAPI(url='<HOST>', username='<USERNAME>', password='<PASSWORD>')
    print(client.link.get(<ID>))
    ticketarticles = client.ticket.articles
    print(ticketarticles)

TicketArticleAttachment Resource
--------------------------------

The :class:`~zammad_py.api.TicketArticleAttachment` resource has the :meth:`~zammad_py.api.TicketArticleAttachment.download()` method.

.. code-block:: python

        """Download the ticket attachment associated with the ticket id

        :param id: Ticket attachment id
        :param article_id: Ticket article id
        :param ticket_id: Ticket id
        """

Object Resource
---------------
The :class:`~zammad_py.api.Object` resource has the :meth:`~zammad_py.api.Object.execute_migrations()` method to run the migrations of an object.

Using "On behalf of"
--------------------

To do actions on behalf of another user, just set the `on_behalf_of` attribute on the instance of ZammadAPI


.. code-block:: python

    from zammad_py import ZammadAPI
    client = ZammadAPI(url='<HOST>', username='<USERNAME>', password='<PASSWORD>')
    client.on_behalf_of = 'test@user.com'
    # Do stuff...

