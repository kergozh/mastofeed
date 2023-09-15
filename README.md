# mastofeed

This code publish content from a RSS feed.  

### Dependencies

-   **Python 3**
-   Mastodon account

### Parameters:

In actions.yaml

-  `url`: feed url
-  `announcement`: first line in Mastodon publication 
-  `hashtags`: last line in Mastodon publication  
-  `days`: number of valid days in feed file. 
-  `repetitions`: number of elements in the repetitions control file.
-  `max`: maximum number of publications
-  `reverse`: descending sorting in feed file.

In config.yaml

- `hostname`: instance url
- `access_type`: credentials, acces token o github action (SO environment variables)
- `access_token`: client-id, secret and token in "access token" acces_type.
- `disable_post`: test option for no publish toots.

### Usage:

Server o desktop:

1. Optionally, create a new user for running the bot: `adduser --disabled-login user_name`

2. Clone the repository `git clone https://github.com/kergozh/mastofeed.git` 

3. Crate a virtual environment `python3 -m venv .venv` and activate it `source .venv/bin/activate`

4. Run `pip install -r requirements.txt` to install needed libraries.  

5. Modify options in the `actions.yaml` and `config.yaml` files. 

6. It's possible to fill in the config yaml the cliend id, cliend secret and access token of an application created in the Mastodon web (with de "development" opction). Also, it's possilbe to indicate credentials access and run `python3 quote.py` manually once to setup and get its access token to Mastodon instance.

7. Use your favourite scheduling method to set `feed.sh` to run. For example,  add  `0 6 * * * /home/user_name/mastofeed/feed.sh 2>&1 | /usr/bin/logger -t MASTOFEED` in `crontab -e`. The system and error log will be in `/var/log/syslog`. Don't forgot the execution privilegies `chmod +x feed.sh`. Don't forgot update the user_name in `feed.sh`

Github Action:

1. Fork the repo.

2. Add client-id, secret and token in settings > security > secrets and variables > actions > repository secrets as: `MASTO_CLIENT_ID`, `MASTO_SECRET` and `MASTO_TOKEN`.

3. Change `access_type` in config.yaml a `GA`

4. Check `disable_post` parameter in config.yaml

5. Uncomment the cron options in .github/workflows/mastofeed.yml
