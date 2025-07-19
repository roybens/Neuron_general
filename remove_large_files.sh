#!/bin/bash
while IFS= read -r file; do
    git rm --cached --ignore-unmatch "$file"
done < large_files_to_remove.txt
