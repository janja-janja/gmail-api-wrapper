# Gmail API Wrapper Changelog
--------------------------------------------------------------------------------

### v0.1.1a1 [18-09-2017]

Features:

- [x] Add `GAW_CLIENT_SECRET_FILE_PATH` env variable to allow passing client secret
file path.
- [x] Add `GAW_DISABLE_SSL_CERTS` env variable to allow diasbling ssl certs validation
- [x] Add a vacation responder activation method
- [x] Add a way to view vacation responder in use if any.
- [x] Update README

### v0.0.1a11 [16-09-2017]

Features:

- [x] Add `GWA_CA_CERTS_PEM_FILE` env variable to allow passing custom SSL cert
file path
- [x] Update `LICENSE`
- [x] Update `README`
- [x] Add Gmail Api Wrapper Write operations shell

### v0.0.1a7 [11-09-2017]

Bugs:

- [x] Get message body from `return message_payload['body']['data']`
when `return message_payload['parts'][0]['body']['data']` returns a `KeyError`
exception



### v0.0.1a4 [10-09-2017]

Features:

- [x] Add Circle CI Configs
- [x] Extract base64 message body


### v0.0.1a3 [05-09-2017]

Features:

- [x] Bump `google-api-python-client` to 1.6.3 from 1.6.2
- [x] Allow fetching new messages from specific email addresses
- [x] Add `utils.py` module to hold helper methods

### v0.0.1a2 [05-09-2017]

Bugs:

- [x] Fix availbale LABELS checking in `GmailAPIReadWrapper` helper class

Breaking:

- [x] Renamed `GmailAPIWriteWrapper` to `GmailAPIModifyWrapper` and moved it
    from `gmail_api_wrapper.crud.write` to `gmail_api_wrapper.crud.modify` module



### v0.0.1a1 [04-09-2017]

Features:

- [x] Make `gmail_api_wrapper` a package
- [x] Add `setup.py` file
- [x] Add package `requirements/*`
- [x] Add `GmailAPIConnection` helper class in `gmail_api_wrapper.connection.py` module
- [x] Add `GmailAPIReadWrapper` helper class in `gmail_api_wrapper.crud.read.py` module
- [x] Add `GmailAPIWriteWrapper` helper class in `gmail_api_wrapper.crud.modify.py` module


### v0.0.1a0 [27-07-2017]

Features:

- [x] Project Initialization

