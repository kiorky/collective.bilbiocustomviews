#!/usr/bin/env bash
PROJECT="collective.bibliocustomviews"
IMPORT_URL="https://github.com/collective/collective.bibliocustomviews.git"
cd $(dirname $0)/..
[[ ! -d t ]] && mkdir t
rm -rf t/*
tar xzvf $(ls -1t ~/cgwb/$PROJECT*z) -C t
files="
./
"
for f in $files;do
    rsync -aKzv t/$PROJECT/$f $f
done
# vim:set et sts=4 ts=4 tw=80: 
