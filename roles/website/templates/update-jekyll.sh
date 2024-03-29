#! /usr/bin/env sh

# shellcheck disable=SC1091
. /etc/profile

set -eu

SOURCE="$HOME/.var/jekyll-envs/{{ website_domain }}/"
DESTINATION="/var/www/{{ website_user }}/domains/{{ website_domain }}/"

cd "$SOURCE"

git fetch --quiet origin
git reset --quiet --hard origin/master
git submodule --quiet update --init

bundle config set --local path .bundle
bundle install --quiet

exec bundle exec jekyll build --quiet --destination "$DESTINATION"
