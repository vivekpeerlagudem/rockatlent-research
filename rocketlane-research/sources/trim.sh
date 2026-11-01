#!/bin/bash
# Print the article body of a saved help-centre text file (drops nav, plan badges and the series list)
awk '/^Created by/{p=1} /^Was this article helpful/{p=0} p' "$1" | grep -v '^$' \
 | awk '/^Articles in this series/{s=1} s&&/^No article available/{s=0;next} !s' \
 | grep -v -E '^(Essential|Standard|Premium|Enterprise|Plan Availability)$'
