#!/usr/bin/env bash

if [ "$USER" != "root" ]; then
	echo "This script installs system dependencies, and requires root"
	exit 9
fi


#########################
# Requirements 
#########################

# Debian Jessie
read -r -d '' DEBIAN_PACKAGES <<-'PACKAGES'
	libjpeg62-turbo-dev libopenjpeg-dev libfreetype6-dev libtiff5-dev
	liblcms2-dev libwebp-dev python3-dev
PACKAGES

# MySQL dependencies
read -r -d '' MYSQL_PACKAGES <<-'PACKAGES'
	libmysqlclient-dev
PACKAGES

# Postgres dependencies
read -r -d '' PGSQL_PACKAGES <<-'PACKAGES'
	libpq-dev
PACKAGES


#########################
# Check for permissions
#########################
if [ "$USER" != "root" ]; then
	echo "This script installs system dependencies, and requires root"
	exit 9
fi


#########################
# Compile reqs
#########################

PACKAGES="$DEBIAN_PACKAGES"

echo "Which database requirements would you like to install?"
echo "	mysql"
echo "	postgres"
echo "	none (default)"
echo -e "> "

select DB in "mysql" "postgres" "none"; do
	case $DB in
		mysql ) PACKAGES+=' '$MYSQL_PACKAGES; break;;
		postgres ) PACKAGES+=' '$PGSQL_PACKAGES; break;;
		none|* ) break;;
	esac
done

echo "Installing requested dependencies..."

# Display command
set -x

# Try installing the debian requirements
apt --no-install-recommends install $PACKAGES
