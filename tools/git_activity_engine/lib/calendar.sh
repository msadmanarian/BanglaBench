#!/usr/bin/env bash
# =====================================================================
# BanglaBench Activity Engine: Calendar & Date Math Utilities
# =====================================================================

get_date_n_days_ago() {
  local days_ago=$1
  if date -d "1 day ago" >/dev/null 2>&1; then
    # GNU date (standard in Git Bash)
    date -d "$days_ago days ago" +"%Y-%m-%d"
  else
    # BSD date fallback
    date -v-"${days_ago}"d +"%Y-%m-%d"
  fi
}

get_day_of_week() {
  local date_str=$1
  date -d "$date_str" +"%u" # 1 = Monday, 7 = Sunday
}

get_random_time_for_date() {
  local date_str=$1
  local hour=$(( 9 + RANDOM % 13 )) # 09:00 to 21:00
  local min=$(( RANDOM % 60 ))
  local sec=$(( RANDOM % 60 ))
  printf "%s %02d:%02d:%02d" "$date_str" "$hour" "$min" "$sec"
}
