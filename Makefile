#!/usr/bin/make -f

.PHONY: deb

deb:
	chmod +x videb.py
	./videb.py debian.yml create

install: deb
	dpkg -i *.deb
