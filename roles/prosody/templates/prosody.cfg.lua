-- {{ ansible_managed }}
-- Prosody Example Configuration File
--
-- Information on configuring Prosody can be found on our
-- website at http://prosody.im/doc/configure
--
-- Tip: You can check that the syntax of this file is correct
-- when you have finished by running: luac -p prosody.cfg.lua
-- If there are any errors, it will let you know what and where
-- they are, otherwise it will keep quiet.
--
-- The only thing left to do is rename this file to remove the .dist ending, and fill in the
-- blanks. Good luck, and happy Jabbering!


---------- Server-wide settings ----------
-- Settings in this section apply to the whole server and are the default settings
-- for any virtual hosts

-- This is a (by default, empty) list of accounts that are admins
-- for the server. Note that you must create the accounts separately
-- (see http://prosody.im/doc/creating_accounts for info)
-- Example: admins = { "user1@example.com", "user2@example.net" }
admins = { "{{jabber_domain_admin}}@{{ jabber_domain }}" }

-- Enable use of libevent for better performance under high load
-- For more information see: http://prosody.im/doc/libevent
--use_libevent = true;

-- This is the list of modules Prosody will load on startup.
-- It looks for mod_modulename.lua in the plugins folder, so make sure that exists too.
-- Documentation on modules can be found at: http://prosody.im/doc/modules
modules_enabled = {

	-- Generally required
		"roster"; -- Allow users to have a roster. Recommended ;)
		"saslauth"; -- Authentication for clients and servers. Recommended if you want to log in.
		"tls"; -- Add support for secure TLS on c2s/s2s connections
		"dialback"; -- s2s dialback support
		"disco"; -- Service discovery

	-- Not essential, but recommended
		"private"; -- Private XML storage (for room bookmarks, etc.)
		"vcard"; -- Allow users to set vCards

	-- These are commented by default as they have a performance impact
		--"privacy"; -- Support privacy lists
		"compression"; -- Stream compression (Debian: requires lua-zlib module to work)

	-- Nice to have
		"version"; -- Replies to server version requests
		"uptime"; -- Report how long server has been running
		"time"; -- Let others know the time here on this server
		"ping"; -- Replies to XMPP pings with pongs
		"pep"; -- Enables users to publish their mood, activity, playing music and more
		"register"; -- Allow users to register on this server using a client and change passwords

	-- Admin interfaces
		"admin_adhoc"; -- Allows administration via an XMPP client that supports ad-hoc commands
		--"admin_telnet"; -- Opens telnet console interface on localhost port 5582

	-- HTTP modules
		"bosh"; -- Enable BOSH clients, aka "Jabber over HTTP"
		--"http_files"; -- Serve static files from a directory over HTTP

	-- Other specific functionality
		"posix"; -- POSIX functionality, sends server to background, enables syslog, etc.
		--"groups"; -- Shared roster support
		--"announce"; -- Send announcement to all online users
		--"welcome"; -- Welcome users who register accounts
		"watchregistrations"; -- Alert admins of registrations
		--"motd"; -- Send a message to users when they log in
		--"legacyauth"; -- Legacy authentication. Only used by some old clients and bots.
};

modules_disabled = {
	-- "offline"; -- Store offline messages
	-- "c2s"; -- Handle client connections
	-- "s2s"; -- Handle server-to-server connections
};

allow_registration = true;
bosh_ports = {
		{
			port = 5280;
			path = "http-bind";
		},
		{
			port = 5281;
			path = "http-bind";
			ssl = {
				key = "/var/lib/prosody/{{ jabber_domain }}.key";
				certificate = "/var/lib/prosody/{{ jabber_domain }}.crt";
			}
		}
	}
consider_bosh_secure = true
cross_domain_bosh = true


daemonize = true;

pidfile = "/var/run/prosody/prosody.pid";

ssl = {
	key = "/var/lib/prosody/localhost.key";
	certificate = "/var/lib/prosody/localhost.crt";
}

c2s_require_encryption = false

s2s_secure_auth = false

--s2s_insecure_domains = { "gmail.com" }

--s2s_secure_domains = { "jabber.org" }

authentication = "internal_plain"

sql = { driver = "MySQL", database = "{{ jabber_mysql_db }}", username = "{{ jabber_mysql_user }}", password = "{{ jabber_mysql_passwd }}", host = "localhost" }

log = {
	info = "/var/log/prosody/prosody.log";
	error = "/var/log/prosody/prosody.err";
	{ levels = { "error" }; to = "syslog";  };
}

VirtualHost "{{ jabber_domain }}"

	ssl = {
		key = "/var/lib/prosody/{{ jabber_domain }}.key";
		certificate = "/var/lib/prosody/{{ jabber_domain }}.crt";
	}

Component "{{ jabber_domain_muc }}" "muc"

Include "conf.d/*.cfg.lua"
