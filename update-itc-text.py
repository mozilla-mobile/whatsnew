#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import os
import os.path
import urllib.request

def fetch_json(url):
    with urllib.request.urlopen(url) as fp:
        return json.load(fp)

if __name__ == "__main__":

    mappings = fetch_json("https://l10n.mozilla-community.org/stores_l10n/api/v1/apple/localesmapping/")
    #print(mappings)

    reverse_mappings = {value: key for key, value in mappings.items()}
    reverse_mappings['nl'] = 'nl-NL' # Temporary until API is updated
    #print(reverse_mappings)

    for locale in fetch_json("https://l10n.mozilla-community.org/stores_l10n/api/v1/fx_ios/whatsnew/release/"):
        print("Updating What's New section for %s" % locale)
        translation = fetch_json("https://l10n.mozilla-community.org/stores_l10n/api/v1/fx_ios/translation/release/%s/" % locale)

        itc_locale = reverse_mappings[locale]
        if not os.path.exists("metadata/%s" % itc_locale):
            print(" * Failed - Locale %s does not exist on the app store yet" % itc_locale)
            continue

        fields_to_files = {
            "title": "name.txt",
            "description": "description.txt",
            "subtitle": "subtitle.txt",
            "whatsnew": "release_notes.txt",
        }

        for field_name, file_name in fields_to_files.items():
            with open("metadata/%s/%s" % (itc_locale, file_name), "w", encoding="utf-8") as fp:
                fp.write(translation[field_name])
                print(" * Updated metadata/%s/%s" % (itc_locale, file_name))

