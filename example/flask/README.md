# Simple endpoint in Python 3 Flask

## Installation

1. Go to https://hole-api.cert.pl/ and write down the values generated in sections ,,Required headers'' and ,,Signature validation key''. Don't close the web browser.
2. Install the application:
```
pip3 install -r requirements.txt
cp config.example.py config.py
# fill the config using values recorded in step (1)
python3 app.py
```

3. Run application:
```
python3 app.py
```

4. Get back on the website and complete the service activation procedure, by pasting the full URL of your application.

*Note:* Consider using uWSGI and virtualenv for production setup.

