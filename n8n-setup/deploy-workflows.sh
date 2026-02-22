#!/bin/bash
# Deploy N8N Workflows to the N8N instance

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKFLOWS_DIR="$SCRIPT_DIR/../n8n-workflows"
N8N_HOST="${N8N_HOST:-localhost}"
N8N_PORT="${N8N_PORT:-5678}"
N8N_PROTOCOL="${N8N_PROTOCOL:-http}"
N8N_USER="${N8N_BASIC_AUTH_USER:-admin}"
N8N_PASS="${N8N_BASIC_AUTH_PASSWORD:-AlKhayma2026!}"

echo "🏖️ AlKhayma Beach Resort - N8N Workflow Deployment"
echo "=================================================="

# Wait for N8N to be ready
echo "📡 Checking N8N availability..."
for i in {1..30}; do
    if curl -s -o /dev/null -w "%{http_code}" "$N8N_PROTOCOL://$N8N_HOST:$N8N_PORT/health" | grep -q "200"; then
        echo "✅ N8N is ready!"
        break
    fi
    echo "⏳ Waiting for N8N... (attempt $i/30)"
    sleep 2
done

# Import workflows
echo ""
echo "📥 Importing workflows..."

for workflow_file in "$WORKFLOWS_DIR"/*.json; do
    if [ -f "$workflow_file" ]; then
        workflow_name=$(basename "$workflow_file" .json)
        echo "  → Importing: $workflow_name"
        
        # Import workflow via N8N API
        curl -s -X POST \
            "$N8N_PROTOCOL://$N8N_HOST:$N8N_PORT/rest/workflows" \
            -u "$N8N_USER:$N8N_PASS" \
            -H "Content-Type: application/json" \
            -d "@$workflow_file" || echo "    ⚠️ Failed to import $workflow_name"
    fi
done

echo ""
echo "✅ Workflow import complete!"
echo ""
echo "🔗 Access N8N at: $N8N_PROTOCOL://$N8N_HOST:$N8N_PORT"
echo "👤 Username: $N8N_USER"
