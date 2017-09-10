# Gmail API Wrapper Changelog
--------------------------------------------------------------------------------
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

