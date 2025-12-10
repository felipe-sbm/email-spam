#!/bin/bash
echo "Adding 100 emails..."
for i in {1..100}
do
   curl -s -X POST http://localhost:5001/emails \
     -H "Content-Type: application/json" \
     -d "{\"sender\": \"sender$i@example.com\", \"recipient\": \"recipient$i@example.com\", \"subject\": \"Test Email $i\", \"body\": \"This is test email number $i. It is not spam.\", \"is_spam\": false, \"spam_score\": 0.01}" > /dev/null
   
   # Print a dot every 10 emails
   if (( $i % 10 == 0 )); then
       echo -n "."
   fi
done
echo "\nDone!"
