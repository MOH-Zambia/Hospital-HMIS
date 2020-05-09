#!/bin/bash

# Exit when any command fails
set -e

# Debugging shizz
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
trap 'if [ $? -ne 0 ]; then echo "\"${last_command}\" command filed with exit code $?."; fi' EXIT

OS_VERSION=$(cat /etc/os-release | grep "^VERSION_ID=" | awk -F "=" '{ print $2 }' | sed 's/"//g')
OS_NAME=$(cat /etc/os-release | grep "^ID=" | awk -F "=" '{ print $2 }' | sed 's/"//g')
OS_ARCH=$(dpkg-architecture -qDEB_HOST_ARCH)

# Common Linux build functions
source pkg/linux/build-functions.sh

# Assemble the "standard" installation footprint
_setup_env $0 "debian"
_cleanup "deb"
_setup_dirs
_create_python_virtualenv "debian"
_build_runtime
_build_docs "debian"
_copy_code

#
# Server package
#

# Create the Debian packaging stuffs for the server
echo "Creating the server package..."
mkdir "${SERVERROOT}/DEBIAN"

cat << EOF > "${SERVERROOT}/DEBIAN/control"
Package: ${APP_NAME}-server
Version: ${APP_LONG_VERSION}
Architecture: ${OS_ARCH}
Depends: python3, libpq5
Recommends: postgresql-client | postgresql-client-12 | postgresql-client-11 | postgresql-client-10
Maintainer: pgAdmin Development Team <pgadmin-hackers@postgresql.org>
Description: The core server package for pgAdmin. pgAdmin is the most popular and feature rich Open Source administration and development platform for PostgreSQL, the most advanced Open Source database in the world.
EOF

# Build the Debian package for the server
fakeroot dpkg-deb --build "${SERVERROOT}" "${DISTROOT}/${APP_NAME}-server_${APP_LONG_VERSION}_${OS_ARCH}.deb"

#
# Desktop package
#

# Create the Debian packaging stuffs for the desktop
echo "Creating the desktop package..."
mkdir "${DESKTOPROOT}/DEBIAN"

cat << EOF > "${DESKTOPROOT}/DEBIAN/control"
Package: ${APP_NAME}-desktop
Version: ${APP_LONG_VERSION}
Architecture: ${OS_ARCH}
Depends: ${APP_NAME}-server, libqt5gui5
Maintainer: pgAdmin Development Team <pgadmin-hackers@postgresql.org>
Description: The desktop user interface for pgAdmin. pgAdmin is the most popular and feature rich Open Source administration and development platform for PostgreSQL, the most advanced Open Source database in the world.
EOF

# Build the Debian package for the server
fakeroot dpkg-deb --build "${DESKTOPROOT}" "${DISTROOT}/${APP_NAME}-desktop_${APP_LONG_VERSION}_${OS_ARCH}.deb"

#
# Web package
#

# Create the Debian packaging stuffs for the web
echo "Creating the web package..."
mkdir "${WEBROOT}/DEBIAN"

cat << EOF > "${WEBROOT}/DEBIAN/control"
Package: ${APP_NAME}-web
Version: ${APP_LONG_VERSION}
Architecture: all
Depends: ${APP_NAME}-server, apache2, libapache2-mod-wsgi-py3
Maintainer: pgAdmin Development Team <pgadmin-hackers@postgresql.org>
Description: The web interface for pgAdmin, hosted under Apache HTTPD. pgAdmin is the most popular and feature rich Open Source administration and development platform for PostgreSQL, the most advanced Open Source database in the world.
EOF

mkdir -p "${WEBROOT}/etc/apache2/conf-available"
cp "${SOURCEDIR}/pkg/debian/pgadmin4.conf" "${WEBROOT}/etc/apache2/conf-available"

# Build the Debian package for the web
fakeroot dpkg-deb --build "${WEBROOT}" "${DISTROOT}/${APP_NAME}-web_${APP_LONG_VERSION}_all.deb"

#
# Meta package
#

# Create the Debian packaging stuffs for the meta package
echo "Creating the meta package..."
mkdir "${METAROOT}/DEBIAN"

cat << EOF > "${METAROOT}/DEBIAN/control"
Package: ${APP_NAME}
Version: ${APP_LONG_VERSION}
Architecture: all
Depends: ${APP_NAME}-server, ${APP_NAME}-desktop, ${APP_NAME}-web
Maintainer: pgAdmin Development Team <pgadmin-hackers@postgresql.org>
Description: Installs all required components to run pgAdmin in desktop and web modes. pgAdmin is the most popular and feature rich Open Source administration and development platform for PostgreSQL, the most advanced Open Source database in the world.
EOF

# Build the Debian meta package
fakeroot dpkg-deb --build "${METAROOT}" "${DISTROOT}/${APP_NAME}_${APP_LONG_VERSION}_all.deb"
