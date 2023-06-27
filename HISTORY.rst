=======
History
=======

3.0.0 (2023-02-27)
------------------
* release/3.0.0
  Add Pagination to search. This is an incompatible change to search API in olders versions.

2.0.0 (2023-02-14)
------------------

* release/2.0.0
  Documentation rewrite with more examples for use
  Rewrote Contributing Guide
  Added new Resource: Link
  Fixed Tests, Create and delete functions to not cause errors by calling the urls with expand=true added.


1.1.0 (2022-08-04)
------------------

* release/1.1.0
  Small Bugfixes, Linting
  Added TicketArticlePlain


1.0.1 (2021-05-28)
------------------

* release/1.0.1
  feat: Take url instead of host
  Update pytest, requests
  Fix Documentation

0.1.7 (2019-04-25)
------------------

* release/0.1.7
  feat: Make username, pass optional


0.1.6 (2019-04-11)
------------------

* release/0.1.6
  Update vcrpy, requests
  Fix Pagination, Add per_page getter / setter
  fix: Add context manager for doing req with behalf header

0.1.5 (2018-05-11)
------------------

* release/0.1.5
  Add more python versions to the test matrix

0.1.4 (2018-01-02)
------------------

* release/0.1.4:
  Released version 0.1.4
  Support indexing on paginated response
  Update pytest from 3.2.5 to 3.3.0
  Close session at exit
  Update pytest from 3.2.4 to 3.2.5
  Update pytest from 3.2.3 to 3.2.4
  API improvements
  Update README.rst
  Add pagination tests

0.1.3 (2017-11-13)
------------------

* release/0.1.3:
  Released version 0.1.3
  Add pagination support
  Add more resource endpoints
  Pin vcrpy to latest version 1.11.1
  Pin pytest to latest version 3.2.3
  Pin flake8 to latest version 3.5.0
  Pin requests to latest version 2.18.4


0.1.2 (2017-10-26)
------------------

* release/0.1.2:
  Released version 0.1.2
  Add toggle flag to use SSL or not
  Add tests for group resource
  Update README.md
  Add tests for ticket resource
  Fix json decode error
 master

0.1.0 (2017-10-25)
------------------

* Released version 0.1.1
  Test for all CRUD ops
  Add update method on base resource
  Add tests
  Update  method in API
  Flake8ify
  Add basic zammad api
  Initial Boilerplate
