#!/bin/sh
SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

## key of:
# genofire:		386ED1BF848ABB4A6B4A3C45FC83907C125BC2BC
# jplitza:		D7E72BFC9E133E0452DAFBCBB17F2106D8CCEC27
# mortzu:		62D00A6960AC2256A24240BCD568B1E5EB1A6E50
# ollibaba:		D9E17720908282C3A8232361DB7D9F68F00F513E


"${SCRIPT_DIR}/open.sh" | gpg -e \
-r 386ED1BF848ABB4A6B4A3C45FC83907C125BC2BC \
-r D7E72BFC9E133E0452DAFBCBB17F2106D8CCEC27 \
-r 62D00A6960AC2256A24240BCD568B1E5EB1A6E50 \
-r D9E17720908282C3A8232361DB7D9F68F00F513E \
-o "${SCRIPT_DIR}/../vault_passphrase.gpg"
