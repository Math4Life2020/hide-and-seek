#!/bin/bash

# URL of our Flask application
URL="http://127.0.0.1:5000"

# Function to generate a random float between min and max
random_float() {
    printf "%.4f" $(awk -v min=$1 -v max=$2 'BEGIN{srand(); print min+rand()*(max-min)}')
}

# Array of names
names=("Alice" "Bob" "Charlie" "David" "Eve" "Frank" "Grace" "Heidi" "Ivan" "Julia")

# Function to send a POST request
send_post_request() {
    name=$1
    lat=$(random_float 30 50)
    lon=$(random_float -100 -70)
    
    echo "Sending POST request for $name"
    response=$(curl -s -X POST $URL -H "Content-Type: application/json" \
         -d "{\"user\":\"$name\", \"lat\":$lat, \"long\":$lon}")
    echo "Response: $response"
    echo
}

# Send POST requests
for name in "${names[@]}"; do
    send_post_request "$name"
done

# Send additional POST requests to update some users
for i in {1..5}; do
    random_index=$((RANDOM % ${#names[@]}))
    send_post_request "${names[$random_index]}"
done

# Start the game
echo "Starting the game"
start_response=$(curl -s -X POST $URL/start)
echo "Start Game Response:"
echo "$start_response" | python3 -m json.tool
echo

# Send GET request
echo "Sending GET request"
get_response=$(curl -s -X GET $URL)
echo "GET Response:"
echo "$get_response" | python3 -m json.tool

echo "Test completed."
