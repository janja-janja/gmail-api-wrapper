Gmail API Wrapper For Python
============================

Behind the scenes
----------------

  * *Language*: Python_
  * *Testing*: Tox_, Pytest_, Coverage_, Flake8_
  * *Deploying*: Ansible_
  * *CI*: CircleCI_
  * *Code*: Github_


Installation
------------

.. code:: bash

    pip install --upgrade gmail-api-wrapper


Setup
-----

`gmail-api-wrapper` uses OAuth authentication

Generate a client ID and client secret Here_ under section
**Step 1: Turn on the Gmail API**. Follow steps *a* to *h*.

After you have downloaded the client_secret file, do the following

.. code:: bash

    mkdir ~/.credentials

Once you're done creating the `.credentials` directory, rename the client_secret
file you downloaded ealier to `client_secret.json` and move it to the `~/.credentials`
folder


Env Variables -- Get scopes from GMAIL_SCOPES_
----------------------------------------------

.. code:: bash

    export GAW_SCOPES=['gmail-scopes-1, 'gmail-scope-2']


    # If you're using custom SSL certs, set GWA_CA_CERTS_PEM_FILE env variable
    export GWA_CA_CERTS_PEM_FILE=<path-to-custom-pem-ssl-cert>


    # The user Id to use. Default to 'me'. A special identifier for gmail
    # that refers to the email address used to do OAuth2 handshake
    export GAW_USER_ID=<your@email.address>


    # Your preferred application name. Defaults to 'Gmail API Wrapper'
    export GAW_APPLICATION_NAME=<your-preferred-application-name>



Usage - READ
------------

.. code:: python

    from gmail_api_wrapper.crud.read import GmailAPIReadWrapper


    gmail_api = GmailAPIReadWrapper().gmail_api_connect()


    # Check unread messages. Returns a list of dicts in the below format
    gmail_api.check_new_mail()

    >>> [

            {
                'subject': 'Sample Subject',
                'base64_msg_body': 'base64string',
                'from:' 'exapmle@mail_server.com'
                'date': '2017-09-16T10:57:12.4323'
            },
        ]

    # Check new mail from specific sender. Returns a list of dicts above
    gmail_api.check_new_mail(sender='example@mail_server.com')



    # Alternatively, you get all unread messages from a specific sender
    gmail_api.get_unread_messages(sender='example@mail_server.com')

    >>> [

            {
                'subject': 'Sample Subject',
                'base64_msg_body': 'base64string',
                'from:' 'exapmle@mail_server.com'
                'date': '2017-09-16T10:57:12.4323'
            },
        ]




    # Get all labels present. Returns a list of strings
    gmail_api.get_labels()

    >>> ['INBOX', 'UNREAD', 'SPAM', 'DRAFTS']



    # Get total message count. Returns a formatted json object
    gmail_api.get_total_messages()

    >>> {
            'Total Messages': 2017,
            'Total Threads': 123,
            'Email Address': 'example@mail_server.com'
        }


    # Get a list of messages. Defaults to INBOX if no label is specified
    gmail_api.list_messages()

    >>> [

            {
                'subject': 'Sample Subject',
                'base64_msg_body': 'base64string',
                'from:' 'exapmle@mail_server.com'
                'date': '2017-09-16T10:57:12.4323'
            },
        ]


    # Get a list of messages in DRAFTS and SPAM
    gmail_api.list_messages(labels=['DRAFTS', 'SPAM'])

    >>> [

            {
                'subject': 'Sample Subject',
                'base64_msg_body': 'base64string',
                'from:' 'exapmle@mail_server.com'
                'date': '2017-09-16T10:57:12.4323'
            },
        ]


    # Get a specific message. `message_id` passed must be a google message id object
    gmail_api.get_message('message_id')



Authors
-------

* yoda <dee.caranja@gmail.com>


.. _Python:  https://www.python.org/
.. _Tox: https://tox.readthedocs.io/en/latest/
.. _Pytest: http://doc.pytest.org/en/latest/
.. _Coverage: https://coverage.readthedocs.io/en/coverage-4.2/
.. _Flake8: http://flake8.pycqa.org/en/latest/
.. _Ansible: http://docs.ansible.com/ansible/index.html
.. _CircleCI: https://circleci.com/gh/yoda-yoda/gmail-api-wrapper
.. _Github: https://github.com/yoda-yoda/gmail-api-wrapper
.. _Here: https://developers.google.com/gmail/api/quickstart/python
.. _GMAIL_SCOPES: https://developers.google.com/gmail/api/auth/scopes/
