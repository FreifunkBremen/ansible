#!/bin/sh
SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
gpg --batch --use-agent --decrypt "${SCRIPT_DIR}/../vault_passphrase.gpg"
