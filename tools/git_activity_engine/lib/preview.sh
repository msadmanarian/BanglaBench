#!/usr/bin/env bash
# =====================================================================
# BanglaBench Activity Engine: Terminal Heat-Map Preview
# Renders a terminal-friendly ASCII contribution preview
# =====================================================================

render_preview() {
  local days=$1
  local weekday_prob=$2
  local weekend_prob=$3
  local min_c=$4
  local max_c=$5

  echo "================================================================="
  echo "      BANGLABENCH GIT CONTRIBUTION PLAN PREVIEW (DRY RUN)        "
  echo "================================================================="
  echo "Horizon: Last $days Days"
  echo "Target Branch: $TARGET_BRANCH | Target File: $ACTIVITY_FILE"
  echo "Weekday Activity: $weekday_prob% | Weekend Activity: $weekend_prob%"
  echo "Commit Range: $min_c - $max_c per active day"
  echo "-----------------------------------------------------------------"
  echo " Date         Day   Active?  Est. Commits  Sample Message"
  echo "-----------------------------------------------------------------"

  local total_projected_commits=0
  local active_days=0

  for (( d=days; d>=1; d-- ))
  do
    local d_str
    d_str=$(get_date_n_days_ago "$d")
    local dow
    dow=$(get_day_of_week "$d_str")
    local dow_name
    case $dow in
      1) dow_name="Mon" ;;
      2) dow_name="Tue" ;;
      3) dow_name="Wed" ;;
      4) dow_name="Thu" ;;
      5) dow_name="Fri" ;;
      6) dow_name="Sat" ;;
      7) dow_name="Sun" ;;
    esac

    local prob
    if [ "$dow" -ge 6 ]; then
      prob=$weekend_prob
    else
      prob=$weekday_prob
    fi

    local roll=$(( RANDOM % 100 ))
    if [ "$roll" -lt "$prob" ]; then
      local n_commits=$(( min_c + RANDOM % (max_c - min_c + 1) ))
      total_projected_commits=$(( total_projected_commits + n_commits ))
      active_days=$(( active_days + 1 ))
      local sample_msg
      sample_msg=$(get_random_message)
      printf " %-12s %-5s %-8s %-12d %s\n" "$d_str" "$dow_name" "[YES]" "$n_commits" "${sample_msg:0:38}..."
    else
      printf " %-12s %-5s %-8s %-12s -\n" "$d_str" "$dow_name" "[REST]" "0"
    fi
  done

  echo "-----------------------------------------------------------------"
  echo "Total Active Days Projected: $active_days / $days ($(( (active_days * 100) / days ))%)"
  echo "Total Commits Projected   : $total_projected_commits"
  echo "================================================================="
  echo "To apply this schedule to Git, run:"
  echo "  ./tools/git_activity_engine/bin/bangla-activity generate"
  echo "================================================================="
}
