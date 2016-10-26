#!/bin/bash
python bibstack.py make all

cd ..
git add --all
git commit -am 'resyncing'
git push -u origin gh-pages
