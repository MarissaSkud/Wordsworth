#! /bin/sh -ue

# This script is used to configure a Ubuntu 18.04 machine to run Wordsworth.
# This script can be run manually as superuser on a fresh machine install,
# or run automatically as the initial provisioning step if using ``$ vagrant up''.

# This script was adapted from the Hackbright Linux setup script;
# see https://fellowship.hackbrightacademy.com/materials/prework/

apt-get update

# ensure that environment and Postgres default to UTF-8
echo "LANG=en_US.UTF-8" > /etc/default/locale
echo "LANGUAGE=en_US.UTF-8:" >> /etc/default/locale

# install useful tool(s) to ease deployment
apt-get install -y git

# install postgres
apt-get install -y postgresql postgresql-plpython postgresql-client postgresql-server-dev-10

# install python3
apt-get install -y python3 python3-dev python3-pip

echo "****************"
echo "$0 completed."
echo "****************"

#[]#
