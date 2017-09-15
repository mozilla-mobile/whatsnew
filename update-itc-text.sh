#!/bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

#
# update-itc-text.sh - update the content on iTunes Connect
#
# Mode of operation:
#
#  1) Grab current meta data from the store (source of truth)
#  2) Talk to the Mozilla stores api to find all the what's new sections that are finished
#  3) Update the local copy with the data from the Mozilla stores api
#  4) Fastlane deliver to push back the changes
#
# Step 4 will present a web page with all the updated app store content to review and will ask
# interactively if the command should continue and update the store.
#

set -e

ITC_USERNAME=sarentz@mozilla.com
APP_ID=org.mozilla.ios.Firefox
APP_VERSION=9.0

rm -rf Preview.html metadata screenshots

echo "*"
echo "* Updating $APP_ID $APP_VERSION"
echo "*"
echo

DELIVER_FORCE_OVERWRITE=1 fastlane deliver download_metadata -u $ITC_USERNAME -a $APP_ID -z $APP_VERSION --skip_screenshots
./update-itc-text.py
fastlane deliver update_metadata -u $ITC_USERNAME -a $APP_ID -z $APP_VERSION --skip_binary_upload

echo
echo "*"
echo "* All done updating $APP_ID $APP_VERSION"
echo "*"
