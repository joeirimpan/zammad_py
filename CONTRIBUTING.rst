.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/joeirimpan/zammad_py/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

The Zammad API Client could always use more documentation, whether as part of the
official Zammad API Client docs, in docstrings, or even on the web in blog posts,
articles, and such.

To help with documentation, look in the `docs` folder. If you want to generate the documentation locally to see how it looks, you need to install sphinx

1. Assuming you installed the dependencies with `poetry install`, you can run to generate the html files.
    $ python3 -m sphinx -T -E -b html -d docs/_build/doctrees -D language=en docs/ ./_readthedocs/html

2. Navigate to the new _readthedocs/html folder and open index.html with a Browser to see a preview of the documentation.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/joeirimpan/zammad_py/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `zammad_py` for local development.

1. Install poetry

    $ pip3 install poetry flask8 sphinx

2. Fork the `zammad_py` repo on GitHub.

3. Clone your fork locally::

    $ git clone git@github.com:your_name_here/zammad_py.git

4. This project uses Poetry (https://python-poetry.org/). Set up the projects dependencies like this:

    $ pip3 install poetry
    $ cd zammad_py/
    $ poetry install

    Poetry will create a virtual environment under your home directory. You can see if that worked by running:

        $ ls ~/.cache/pypoetry/virtualenvs/zammad-py*

    Then activate the environment like this:

        $ ~/.cache/pypoetry/virtualenvs/zammad-py*/bin/activate

5. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

6. When you're done making changes, check that your changes pass flake8 and the tests, including testing other Python versions with tox::

    $ flake8 zammad_py tests
    $ py.test
    $ tox

   To get flake8 and tox, just pip install them into your virtualenv.

7. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

8. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python >3.7

Tips
----

To run a subset of tests::

$ py.test tests.test_zammad_py

