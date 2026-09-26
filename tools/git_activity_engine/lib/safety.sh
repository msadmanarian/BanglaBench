#!/usr/bin/env bash
# =====================================================================
# BanglaBench Activity Engine: Safety & Lifecycle Controls
# =====================================================================

check_working_directory() {
  if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "ERROR: Working directory contains uncommitted changes!"
    echo "Please commit or stash your current work before running the activity engine."
    exit 1
  fi
}

rollback_last_generation() {
  local checkpoint_file="tools/git_activity_engine/storage/.last_checkpoint"
  if [ ! -f "$checkpoint_file" ]; then
    echo "ERROR: No checkpoint file found at $checkpoint_file."
    echo "Cannot determine previous HEAD commit."
    exit 1
  fi

  local target_head
  target_head=$(cat "$checkpoint_file")
  echo "Rolling back to pre-generation checkpoint: $target_head..."

  git reset --hard "$target_head"
  rm -f "$checkpoint_file"

  echo "SUCCESS: Rollback complete. Repository restored to $target_head."
}

push_to_remote() {
  local branch
  branch=$(git rev-parse --abbrev-ref HEAD)
  echo "Pushing activity branch '$branch' to remote 'origin'..."
  git push origin "$branch"
  echo "SUCCESS: Contributions pushed to GitHub! Check your profile contribution graph."
}
