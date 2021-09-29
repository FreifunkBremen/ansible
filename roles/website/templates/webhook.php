<?php

// where to log errors and successful requests
define('LOGFILE', getenv('HOME') . '/.var/log/github-webhook.log');

// what command to execute upon retrieval of a valid push event
$cmd = '$HOME/.local/bin/update-jekyll.sh 2>&1';

// the shared secret, used to sign the POST data (using HMAC with SHA1)
$secret = '{{ website_webhook_secret }}';

// receive POST data for signature calculation, don't change!
$post_data = file_get_contents('php://input');
$signature = hash_hmac('sha1', $post_data, $secret);

// required data in POST body - set your targeted branch and repository here!
$required_data = array(
        'ref' => 'refs/heads/master',
        'repository' => array(
                'full_name' => 'FreifunkBremen/bremen.freifunk.net',
        ),
);

// required data in headers - probably doesn't need changing
$required_headers = array(
        'REQUEST_METHOD' => 'POST',
        'HTTP_X_GITHUB_EVENT' => 'push',
        'HTTP_USER_AGENT' => 'GitHub-Hookshot/*',
        'HTTP_X_HUB_SIGNATURE' => 'sha1=' . $signature,
);

// END OF CONFIGURATION

error_reporting(0);

function log_msg($msg) {
        if (is_writable(LOGFILE))
                file_put_contents(LOGFILE, date(DateTime::ISO8601) . ' ' . $msg . "\n", FILE_APPEND);
}

function array_matches($have, $should, $name = 'array') {
        $ret = true;

        if (is_array($have)) {
                foreach ($should as $key => $value) {
                        if (!array_key_exists($key, $have)) {
                                log_msg('Missing: ' . $key);
                                $ret = false;
                        } else if (is_array($value) && is_array($have[$key]))
                                $ret &= array_matches($have[$key], $value);
                        else if (is_array($value) || is_array($have[$key])) {
                                log_msg('Type mismatch: ' . $key);
                                $ret = false;
                        } else if (!fnmatch($value, $have[$key])) {
                                log_msg("Failed comparison: $key={$have[$key]} (expected $value)");
                                $ret = false;
                        }
                }
        } else {
                log_msg('Not an array: ' . $name);
                $ret = false;
        }

        return $ret;
}

log_msg('=== Received request from ' . $_SERVER['REMOTE_ADDR'] . ' ===');
header('Content-Type: text/plain');
$data = json_decode($post_data, true);

// First do all checks and then report back in order to avoid timing attacks
$headers_ok = array_matches($_SERVER, $required_headers, '$_SERVER');
$data_ok = array_matches($data, $required_data, '$data');

if($headers_ok && $data_ok) {
        log_msg("Updating to commit " . $data["after"]);
        ob_start();
        passthru($cmd, $ret);
        if($ret != 0) {
                http_response_code(500);
        }
} else {
        http_response_code(403);
        die("Forbidden\n");
}

?>
