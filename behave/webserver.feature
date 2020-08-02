Feature: access website

# website
Scenario: access index page
    When I access http://bremen.freifunk.net/
    Then the status code will be 200
    And the page will contain "ist ein Projekt, das versucht ein stadtweites Datennetz auf Basis von WLAN-Routern aufzubauen."

Scenario: access index page over HTTPS
    When I access https://bremen.freifunk.net/
    Then the status code will be 200
    And the page will contain "ist ein Projekt, das versucht ein stadtweites Datennetz auf Basis von WLAN-Routern aufzubauen."

Scenario: access nonexisting page
    When I access http://bremen.freifunk.net/some-nonexisting-page.html
    Then the status code will be 404
    And the page will contain "Seite nicht gefunden"

Scenario: access webhook.php file (test that PHP basically works)
    When I access http://bremen.freifunk.net/webhook.php
    Then the status code will be 403
    And the page content will be "Forbidden\n"

Scenario: access calendar.json file
    When I access http://bremen.freifunk.net/api/calendar.json
    Then the status code will be 200
    And the page will contain '[{"summary":"'

Scenario: access tweets.json file
    When I access http://bremen.freifunk.net/api/tweets.json
    Then the status code will be 200
    And the page will contain '[{"id":"'

Scenario: access Meshviewer
    When I access http://bremen.freifunk.net/map/meshviewer.html
    Then the status code will be 200
    And the page will contain "Meshviewer"

Scenario: access some blog post using old URL
    When I access http://bremen.freifunk.net/blog/2015/03/30/Freifunk-in-den-Medien.html
    Then the status code will be 200
    And the page will contain "Das Interesse an Freifunk wächst. Neben der gewohnten Nachfrage nach Freifunkroutern"

Scenario: access nodes.json
    When I access https://downloads.bremen.freifunk.net/data/meshviewer.json
    Then the status code will be 200
    And the page will contain '"timestamp":"202'


# download site
Scenario: access main page
    When I access http://downloads.bremen.freifunk.net/
    Then the status code will be 200
    And the page will contain "bereitgestellt, die sich häufig ändern oder sehr groß sind"

Scenario: access main page over HTTPS
    When I access https://downloads.bremen.freifunk.net/
    Then the status code will be 200
    And the page will contain "bereitgestellt, die sich häufig ändern oder sehr groß sind"

Scenario: access list of stable firmware
    When I access http://downloads.bremen.freifunk.net/firmware/stable/sysupgrade/
    Then the status code will be 200
    And the page will contain "-tp-link-tl-wr841n-nd-v3-sysupgrade.bin"
    And the page will contain "stable.manifest"
    And the page will contain "Hier findest du die aktuellen Firmware-Dateien."

Scenario: access list of opkg module directories
    When I access https://downloads.bremen.freifunk.net/opkg/modules/
    Then the status code will be 200
    And the page will contain "gluon-ffhb-201"


# wiki
Scenario: access wiki main page
    When I access http://wiki.bremen.freifunk.net/
    Then the status code will be 200
    And the page will contain "Herzlich willkommen im Freifunk Bremen Wiki"

Scenario: access wiki main page over HTTPS
    When I access https://wiki.bremen.freifunk.net/
    Then the status code will be 200
    And the page will contain "Herzlich willkommen im Freifunk Bremen Wiki"

Scenario: try to create new page without logging in
    When I access http://wiki.bremen.freifunk.net/gollum/create/nonexisting-page-lsdfkj
    Then the status code will be 401
    And the page will contain "Die Benutzerabfrage dient lediglich der Spamvermeidung."

Scenario: try to create new page
    When I access http://wiki.bremen.freifunk.net/gollum/create/nonexisting-page-lsdfkj as wellenfunk/foobar
    Then the status code will be 200
    And the page will contain ">Create New Page</h1>"

Scenario: try to edit home page
    When I access http://wiki.bremen.freifunk.net/gollum/edit/Home as wellenfunk/foobar
    Then the status code will be 200
    And the page will contain ">Editing <strong>Home</strong></h1>"


# status
Scenario: access status page
    When I access http://status.bremen.freifunk.net/
    Then the status code will be 200
    And the page will contain "<h1>Freifunk Bremen Status</h1>"

Scenario: access status page over HTTPS
    When I access https://status.bremen.freifunk.net/
    Then the status code will be 200
    And the page will contain "<h1>Freifunk Bremen Status</h1>"

Scenario: access JSON data file
    When I access http://status.bremen.freifunk.net/data/merged.json
    Then the status code will be 200
    And the page will contain '"uuid":"'

Scenario: access to token/ directory is denied
    When I access http://status.bremen.freifunk.net/token/
    Then the status code will be 403
    And the page will contain "Forbidden"

Scenario: access to .git/ directory is hidden
    When I access http://status.bremen.freifunk.net/.git/
    Then the status code will be 404
    And the page will contain "Not Found"

Scenario: access to config.ini file is forbidden
    When I access http://status.bremen.freifunk.net/config.ini
    Then the status code will be 403
    And the page will contain "Forbidden"


# tasks
Scenario: access tasks login page
    When I access http://tasks.bremen.freifunk.net/
    Then the status code will be 200
    And the page URL will be "https://tasks.ffhb.de/"
    And the page will contain "Login to Phabricator</span>"
    And the page will contain "Freifunk Bremen</a>"

Scenario: access tasks login page over HTTPS
    When I access https://tasks.bremen.freifunk.net/
    Then the status code will be 200
    And the page URL will be "https://tasks.ffhb.de/"
    And the page will contain "Login to Phabricator</span>"
    And the page will contain "Freifunk Bremen</a>"
