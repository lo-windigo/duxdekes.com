#!/usr/bin/env bash

# Any Debian requirements should be listed here
# Debian Jessie
read -r -d '' DEBIAN_PACKAGES <<-'PACKAGES'
	libjpeg62-turbo-dev libopenjpeg-dev libfreetype6-dev libtiff5-dev
	liblcms2-dev libwebp-dev tk8.6-dev python3-tk
PACKAGES


# Python package requirements
read -r -d '' PIP_PACKAGES <<-'PACKAGES'
	Django
	pillow
PACKAGES


# Try installing the debian requirements
if [ "$USER" == "root" ]; then

	apt install $DEBIAN_PACKAGES
fi


# Use pip to install any other requirements
pip install $PIP_PACKAGES

