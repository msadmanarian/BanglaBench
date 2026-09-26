#!/usr/bin/env bash
# =====================================================================
# BanglaBench Activity Engine: Commit Generator Core
# Generates authentic backdated Git commits safely
# =====================================================================

execute_generation() {
  local days=$1
  local weekday_prob=$2
  local weekend_prob=$3
  local min_c=$4
  local max_c=$5

  # Ensure target file exists
  mkdir -p "$(dirname "$ACTIVITY_FILE")"
  if [ ! -f "$ACTIVITY_FILE" ]; then
    echo "# BanglaBench Research Activity Journal" > "$ACTIVITY_FILE"
    echo "This journal records chronological research activity, evaluation checkpoints, and code milestones." >> "$ACTIVITY_FILE"
    echo "" >> "$ACTIVITY_FILE"
  fi

  # Record pre-generation HEAD for undo capability
  local initial_head
  initial_head=$(git rev-parse HEAD)
  echo "$initial_head" > "tools/git_activity_engine/storage/.last_checkpoint"

  echo "Starting generation across the past $days days..."
  echo "Pre-run checkpoint recorded: $initial_head"

  local total_commits=0
  local active_days=0

  for (( d=days; d>=1; d-- ))
  do
    local d_str
    d_str=$(get_date_n_days_ago "$d")
    local dow
    dow=$(get_day_of_week "$d_str")

    local prob
    if [ "$dow" -ge 6 ]; then
      prob=$weekend_prob
    else
      prob=$weekday_prob
    fi

    local roll=$(( RANDOM % 100 ))
    if [ "$roll" -lt "$prob" ]; then
      local n_commits=$(( min_c + RANDOM % (max_c - min_c + 1) ))
      active_days=$(( active_days + 1 ))

      for (( c=1; c<=n_commits; c++ ))
      do
        local commit_time
        commit_time=$(get_random_time_for_date "$d_str")
        local msg
        msg=$(get_random_message)

        # Update activity journal
        echo "- **$commit_time**: $msg" >> "$ACTIVITY_FILE"

        git add "$ACTIVITY_FILE"

        # Commit with exact author and committer dates
        GIT_AUTHOR_NAME="$AUTHOR_NAME" \
        GIT_AUTHOR_EMAIL="$AUTHOR_EMAIL" \
        GIT_COMMITTER_NAME="$AUTHOR_NAME" \
        GIT_COMMITTER_EMAIL="$AUTHOR_EMAIL" \
        GIT_AUTHOR_DATE="$commit_time" \
        GIT_COMMITTER_DATE="$commit_time" \
        git commit -m "$msg" --quiet

        total_commits=$(( total_commits + 1 ))
      done

      printf "  [+] %s: Logged %d commits\n" "$d_str" "$n_commits"
    fi
  done

  echo ""
  echo "================================================================="
  echo "SUCCESS: Generated $total_commits commits across $active_days active days!"
  echo "Latest HEAD: $(git rev-parse HEAD)"
  echo "To push to GitHub, run:"
  echo "  ./tools/git_activity_engine/bin/bangla-activity push"
  echo "To rollback this batch, run:"
  echo "  ./tools/git_activity_engine/bin/bangla-activity undo"
  echo "================================================================="
}
