website
=========================

Install Jeykll as used for the main website of Freifunk Bremen.


Configuration
-------------------------

See `defaults/main.yml` for available parameters.

Note that the `website_webhook_secret` parameter doesn't have a default value
Since its value must remain secret, the value must be specified on command line when running ansible-playbook (with `-e "website_webhook_secret=thesecret"`)


Configuration of Github webhook
--------------------------------

Go to the Webhook page at https://github.com/FreifunkBremen/bremen.freifunk.net/settings/hooks/ (you need admin permissions for this), and add a new webhook with these settings:
* payload url: http://bremen.freifunk.net/webhook.php
* content type: application/json
* secret: the value that was passed on command line for `website_webhook_secret` parameter
* for events: "Just the push event."

The webhook will only work if it originates from the FreifunkBremen/bremen.freifunk.net repository and is for the master branch.


Usage
-------------------------

    - hosts: servers
      roles:
         - website


License
-------------------------

GPLv3
