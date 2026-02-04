# Zammad API Client

[![PyPI version](https://img.shields.io/pypi/v/zammad_py.svg)](https://pypi.python.org/pypi/zammad_py)
[![Documentation Status](https://readthedocs.org/projects/zammad-py/badge/?version=latest)](https://zammad-py.readthedocs.io/en/latest/?badge=latest)

Python API client for zammad

* Free software: MIT license
* Documentation: https://zammad-py.readthedocs.io.

## Quickstart

```python
from zammad_py import ZammadAPI

# Initialize the client with the URL, username, and password
# Note the Host URL should be in this format: 'https://zammad.example.org/api/v1/'
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
      "internal": False
   }
}
new_ticket = client.ticket.create(params=params)
```

## General Methods

Most resources support these methods:

- `.all()`: Returns a paginated response with the current page number and a list of elements.
- `.next_page()`: Returns the next page of the current pagination object.
- `.prev_page()`: Returns the previous page of the current pagination object.
- `.search(params)`: Returns a paginated response based on the search parameters.
- `.find(id)`: Returns a single object with the specified ID.
- `.create(params)`: Creates a new object with the specified parameters.
- `.update(params)`: Updates an existing object with the specified parameters.
- `.destroy(id)`: Deletes an object with the specified ID.

## Available Resources

| Resource | Property |
|----------|----------|
| User | `client.user` |
| Organization | `client.organization` |
| Group | `client.group` |
| Role | `client.role` |
| Ticket | `client.ticket` |
| Link | `client.link` |
| TicketArticle | `client.ticket_article` |
| TicketArticleAttachment | `client.ticket_article_attachment` |
| TicketArticlePlain | `client.ticket_article_plain` |
| TicketPriority | `client.ticket_priority` |
| TicketState | `client.ticket_state` |
| TagList | `client.taglist` |
| TicketTag | `client.ticket_tag` |
| KnowledgeBases | `client.knowledge_bases` |
| KnowledgeBasesAnswers | `client.knowledge_bases_answers` |
| KnowledgeBasesCategories | `client.knowledge_bases_categories` |

## Resource-Specific Methods

### User
- `.me()`: Returns information about the current user.

### Ticket
- `.articles(id)`: Returns all articles associated with a ticket.
- `.tags(id)`: Returns all tags associated with a ticket.
- `.merge(id, number)`: Merges two tickets (requires password auth).

### Link
- `.get(id)`: Returns all links associated with a ticket.
- `.add(...)`: Creates a link between two objects.
- `.remove(...)`: Removes a link between two objects.

### TicketArticleAttachment
- `.download(id, article_id, ticket_id)`: Downloads a ticket attachment.

### TagList
- `.all()`: Returns all tags (paginated).
- `.create(params)`: Creates a new tag.
- `.destroy(id)`: Deletes a tag.

### TicketTag
- `.add(id, tag)`: Adds a tag to a ticket.
- `.remove(id, tag)`: Removes a tag from a ticket.

### KnowledgeBases
- `.init()`: Returns the entire knowledge base structure.
- `.manage(id, settings)`: Updates knowledge base settings.
- `.show_permissions(id)`: Returns permissions for a knowledge base.
- `.change_permissions(id, permissions)`: Updates permissions.
- `.reorder_sub_categories(id, category_id, params)`: Reorders sub-categories.
- `.reorder_root_categories(id, params)`: Reorders root categories.

### KnowledgeBasesAnswers
- `.find_answer(knowledge_base_id, answer_id)`: Retrieves a specific answer.
- `.create(params)`: Creates a new answer (requires `knowledge_base_id` in params).
- `.update(id, params)`: Updates an answer (requires `answer_id` in params).
- `.destroy_answer(knowledge_base_id, answer_id)`: Deletes an answer.
- `.change_answer_visibility(knowledge_base_id, answer_id, visibility)`: Updates answer visibility.
- `.add_attachment(knowledge_base_id, answer_id, attachment)`: Uploads an attachment.
- `.delete_attachment(knowledge_base_id, answer_id, attachment_id)`: Removes an attachment.

### KnowledgeBasesCategories
- `.find_category(knowledge_base_id, category_id)`: Retrieves a specific category.
- `.create(params)`: Creates a new category (requires `knowledge_base_id` in params).
- `.update(id, params)`: Updates a category (requires `category_id` in params).
- `.destroy_category(knowledge_base_id, category_id)`: Deletes a category.
- `.show_permissions(knowledge_base_id, category_id)`: Returns category permissions.
- `.change_permissions(knowledge_base_id, category_id, permissions)`: Updates permissions.
- `.reorder_answers(knowledge_base_id, category_id, params)`: Reorders answers.

## On Behalf Of

You can set the `on_behalf_of` attribute to perform actions on behalf of another user:

```python
client.on_behalf_of = 'user@example.com'
```

Or use the context manager:

```python
with client.request_on_behalf_of('user@example.com'):
    client.ticket.create(params=params)
```

## Contributing

The Zammad API Client (zammad_py) welcomes contributions.

You can contribute by reporting bugs, fixing bugs, implementing new features, writing documentation, and submitting feedback.

To get started, see the contributing section in the docs!

Please ensure that your changes include tests and updated documentation if necessary.

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
