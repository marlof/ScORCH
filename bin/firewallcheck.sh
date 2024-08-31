#!/bin/bash
##
## Copyright 2024 Marc Loftus
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##    http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
# File to store cached IP information
CACHE_FILE="ip_cache.txt"

# Initialize the cache file if it does not exist
if [ ! -f "$CACHE_FILE" ]; then
  touch "$CACHE_FILE"
fi

# Function to fetch IP information
fetch_ip_info() {
  local ip=$1
  local ip_info

  # Check if IP info is already cached
  ip_info=$(grep "^$ip " "$CACHE_FILE" | cut -d' ' -f2-)
  
  if [ -z "$ip_info" ]; then
    # Fetch IP info using curl if not in cache
    ip_info=$(curl -s "https://ipinfo.io/$ip" | jq -r '.city + ", " + .region + ", " + .country')
    
    # Cache the result
    echo "$ip $ip_info" >> "$CACHE_FILE"
  fi

  echo "$ip_info"
}

# Function to fetch specific IP address information within a given subnet
fetch_ip_in_prefix() {
  local ip_prefix=$1
  local ip_info
  local specific_ip

  # Choose a specific IP within the given subnet (e.g., .1)
  specific_ip=$(echo "$ip_prefix" | awk -F. '{print $1 "." $2 "." $3 ".1"}')

  # Check if IP info is already cached
  ip_info=$(grep "^$specific_ip " "$CACHE_FILE" | cut -d' ' -f2-)
  
  if [ -z "$ip_info" ]; then
    # Fetch IP info using curl if not in cache
    ip_info=$(curl -s "https://ipinfo.io/$specific_ip" | jq -r '.city + ", " + .region + ", " + .country')
    
    # Cache the result
    echo "$specific_ip $ip_info" >> "$CACHE_FILE"
  fi

  echo "$ip_info"
}

# Read the log file, extract IPs and ports, count occurrences, and get the top 200 IPs
log_file="firewall.log"  # Replace with the actual log file path
top_ips=$(grep -oP 'SRC=\K[\d.]+(?= )' "$log_file" | sort | uniq -c | sort -nr | head -n 200 | awk '{print $2}')

declare -A region_count
declare -A port_count

# Process each top IP address
for ip in $top_ips; do
  printf "Processing IP: $ip "

  
  # Attempt to fetch general IP information (e.g., /24 subnet)
  ip_prefix=$(echo "$ip" | awk -F. '{print $1 "." $2 "." $3 ".0/24"}')
  general_info=$(fetch_ip_in_prefix "$ip_prefix")
  city=$(echo "$general_info" | awk -F', ' '{print $1}')
  region=$(echo "$general_info" | awk -F', ' '{print $2}')
  country=$(echo "$general_info" | awk -F', ' '{print $3}')
  
  echo "$city, $country"
  grep $ip "$log_file" | grep -Eo DPT=[0-9]* | awk -F"=" '{print $2}' | sort -rn | uniq -c

  # Sanitize region and check if it's not empty
  region=$(echo "$region" | tr -d '[:space:]')
  if [ -z "$region" ]; then
    echo "Warning: Region is empty for IP $ip"
    continue
  fi
  
  # Update region count
  region_count["$region"]=$((region_count["$region"] + 1))
  # echo "IP: $ip, Count: $count, City: $city, Region: $region, Country: $country"
  # echo "Current count for $region: ${region_count["$region"]}"

  # Aggregate port counts
  ports=$(grep "SRC=$ip" "$log_file" | grep -oP 'DPT=\K\d+' | sort | uniq -c | sort -nr)
  while IFS= read -r line; do
    port=$(echo "$line" | awk '{print $2}')
    count=$(echo "$line" | awk '{print $1}')
    
    # Check if port is not empty before updating the array
    if [ -n "$port" ] ; then
      port_count["$port"]=$((port_count["$port"] + count))
    fi
  done <<< "$ports"
done

# Display aggregated region counts, sorted in descending order
echo -e "\nAggregated region counts:"
for region in "${!region_count[@]}"; do
    echo "Region: $region - Total Attempts: ${region_count[$region]}"
done | sort -k6 -nr

# Display aggregated port counts, sorted in descending order
echo -e "\nAggregated port counts:"
for port in "${!port_count[@]}"; do
    echo "Port: $port - Total Attempts: ${port_count[$port]}"
done | sort -k6 -nr
