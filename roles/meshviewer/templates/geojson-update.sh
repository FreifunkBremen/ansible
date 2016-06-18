#!/bin/bash

MAP_GIT='/opt/meshviewer_geojson_git'

if [ ! -d "$MAP_GIT" ]; then
  echo "${MAP_GIT} does not exists!" >&2
  exit 1
fi

git -C "$MAP_GIT" pull
if jq . "$MAP_GIT/{{meshviewer_geojson_file}}"; then
  cp "$MAP_GIT/{{meshviewer_geojson_file}}" "{{meshviewer_geojson_file_path}}/meshviewer.geojson"
fi
