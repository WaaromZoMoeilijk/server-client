#!/bin/bash

# Install packages
apt install -y msmtp msmtp-mta

# Set SMTP config
cat > /etc/msmtprc <<EOF
# Default values for all accounts
defaults
auth on
tls on

# Gmail
account waaromzomoeilijk
host mail.waaromzomoeilijk.nl
from davidcloudserver@waaromzomoeilijk.nl

port 465
user davidcloudserver@waaromzomoeilijk.nl
password **your password**

# Syslog logging with facility LOG_MAIL instead of the default LOG_USER.
syslog LOG_MAIL

# Set a default account
account default : gmail
EOF

# Test
echo "This is a test email" | msmtp --debug your@emailaddress.com

exit 0
