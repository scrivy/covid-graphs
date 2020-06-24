#!/bin/bash

cd covid-graphs

git log -1 > last-commit
git submodule status > last-submodule

git pull -q
git submodule update --remote

git log -1 > current-commit
git submodule status > current-submodule

if ! diff -q {last,current}-commit || ! diff -q {last,current}-submodule
then
	date
	echo 'generating graphs.....'
	pipenv run python generate_graphs.py
	echo 'done'
fi
