#!/bin/bash

TEMP_FILE=(mktemp)
echo "[]" > "$TEMP_FILE"
OUTPUT_FILE="output.json"
PAGE=1
AFTER=""


while true;
do
    URL="https://www.reddit.com/subreddits.json"
    if [ -n "$AFTER" ]; then
      URL="$URL?limit=100&&after=$AFTER"
    fi


    RESPONSE=$(curl -s "$URL" \
      -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
      -H 'accept-language: en-GB,en;q=0.9,en-US;q=0.8,sv;q=0.7,ro;q=0.6' \
      -H 'user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36' \
      )
      
    echo $RESPONSE | jq '[.data.children[].data | {
    "name": .name, "title": .title, "subscribers": .subscribers, "display_name": .display_name, "display_name_prefixed": .display_name_prefixed, "created": .created, "submit_text": .submit_text, "header_title": .header_title, "advertiser_category": .advertiser_category, "community_reviewed": .community_reviewed, "id": .id, "subreddit_type": .subreddit_type, "over18": .over18, "allow_videos": .allow_videos, "allow_polls": .allow_polls, "url": .url, "created_utc": .created_utc, "restrict_commenting": .restrict_commenting, "lang": .lang, "notification_level": .notification_level, "comment_contribution_settings": .comment_contribution_settings, "description": .description
    }]' >  $TEMP_FILE 

    jq -s 'add' "$OUTPUT_FILE" "$TEMP_FILE" > "$OUTPUT_FILE.tmp"
    mv "$OUTPUT_FILE.tmp" "$OUTPUT_FILE"

    AFTER=$(echo "$RESPONSE" | jq -r '.data.after')

    echo "Fetching: $URL | USING $AFTER"

    if [ -z "$RESPONSE" ] || [ "$RESPONSE" = "[]" ] || [ -z "$AFTER" ] || [ "$AFTER" = "null" ]; then
        echo "No listings found or end reached."
        break
    fi

    sleep 2
done
