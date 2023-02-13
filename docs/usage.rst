=====
Usage
=====

To use Zammad API Client in a project::

    from zammad_py import ZammadAPI
    client = ZammadAPI(url='<HOST>', username='<USERNAME>', password='<PASSWORD>')

Zammad Resources are implemented as an abstract class (Resource), meaning most objects have the same mechanisms.
Because Zammad uses pagination (https://docs.zammad.org/en/latest/api/intro.html#pagination), the pagination is very helpful.

General Methods
---------------

Most Resources support these methods.

.all()
   | Returns a paginated response with _page containing the page number and _items containing a list of elements.

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


.search(params)
   | Can be called from the current page (pagination object)
   | Contains the previous page object if there are any.

.. code-block:: python

    from zammad_py import ZammadAPI
    client = ZammadAPI(url='<HOST>', username='<USERNAME>', password='<PASSWORD>')
    client.ticket.search({'query': 'Search Content'})


.find(id)
   | Can be called from the current page (pagination object)
   | Contains the previous page object if there are any.

.. code-block:: python

    from zammad_py import ZammadAPI
    client = ZammadAPI(url='<HOST>', username='<USERNAME>', password='<PASSWORD>')
    client.ticket.find(<TICKETID>)


.create(params)
   | Can be called from the current page (pagination object)
   | Contains the previous page object if there are any.

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
   | Can be called from the current page (pagination object)
   | Contains the previous page object if there are any.

.. code-block:: python

    from zammad_py import ZammadAPI
    client = ZammadAPI(url='<HOST>', username='<USERNAME>', password='<PASSWORD>')
    org = client.organization.find(<ID>)
    params = {'name':'NewCompanyName Ltd.'}
    org.update(params=params)

.destroy(id)
   | Can be called from the current page (pagination object)
   | Contains the previous page object if there are any.

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
