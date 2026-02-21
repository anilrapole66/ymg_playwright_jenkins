#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./deploy_azure.sh
#   ./deploy_azure.sh /path/to/key.pem
#   ./deploy_azure.sh /path/to/key.pem azureuser@4.186.30.115 main

KEY_PATH="${1:-$HOME/Downloads/ymgportal_key.pem}"
REMOTE_HOST="${2:-azureuser@4.186.30.115}"
BRANCH="${3:-main}"
REMOTE_APP_DIR="/srv/empportal/ymgportal"

if [[ ! -f "$KEY_PATH" ]]; then
  echo "SSH key not found: $KEY_PATH" >&2
  exit 1
fi

echo "Deploying branch '$BRANCH' to $REMOTE_HOST ..."

ssh -i "$KEY_PATH" "$REMOTE_HOST" "bash -lc '
  set -euo pipefail
  cd \"$REMOTE_APP_DIR\"
  source venv/bin/activate
  git pull origin \"$BRANCH\"
  python manage.py check
  python manage.py migrate --noinput
  python manage.py collectstatic --noinput
  sudo systemctl restart gunicorn-ymgportal
  sudo systemctl restart nginx
  echo \"Deployment complete on \$(hostname).\"
'"

echo "Done."
