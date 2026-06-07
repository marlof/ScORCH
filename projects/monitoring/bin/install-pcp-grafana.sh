#!/bin/bash
set -euo pipefail

# ================================
# Idempotent PCP + Grafana Setup
# ================================

echo "Starting PCP + Grafana setup..."

# --- Update package lists ---
sudo apt update

# --- Install PCP ---
if ! dpkg -l | grep -qw pcp; then
    echo "Installing PCP..."
    sudo apt install -y pcp
else
    echo "PCP already installed. Reinstalling to ensure PMDAs exist..."
    sudo apt install --reinstall -y pcp
fi

# --- Ensure PCP directories exist with correct permissions ---
sudo mkdir -p /var/log/pcp/pmcd
sudo chown -R pcp:pcp /var/log/pcp
sudo chmod -R 750 /var/log/pcp

sudo mkdir -p /run/pcp
sudo chown -R pcp:pcp /run/pcp
sudo chmod -R 770 /run/pcp

# --- Enable and start PCP services ---
for svc in pmcd pmlogger pmproxy; do
    sudo systemctl enable $svc
    sudo systemctl restart $svc || true
done

# --- Verify PMDAs exist ---
missing_pmda=0
for pmda in /var/lib/pcp/pmdas/pmcd/pmda_pmcd.so /var/lib/pcp/pmdas/root/pmdaroot; do
    if [ ! -f "$pmda" ]; then
        echo "Missing PMDA: $pmda"
        missing_pmda=1
    fi
done

if [ "$missing_pmda" -eq 1 ]; then
    echo "Error: Required PMDAs missing. Please check PCP installation."
    exit 1
fi

# --- Install Grafana ---
if ! dpkg -l | grep -qw grafana; then
    echo "Installing Grafana..."
    sudo apt install -y grafana
    sudo systemctl enable --now grafana-server
else
    echo "Grafana already installed. Restarting..."
    sudo systemctl restart grafana-server
fi

# --- Optional: Adjust firewall to allow Grafana ---
if command -v ufw >/dev/null 2>&1; then
    sudo ufw allow 3000/tcp
fi

# --- Done ---
echo "PCP and Grafana setup complete. Services status:"
systemctl status pmcd pmlogger pmproxy grafana-server --no-pager
echo "You can now log in to Grafana at http://<server-ip>:3000 (default admin/admin)."
