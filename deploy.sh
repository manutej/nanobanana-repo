#!/bin/bash
# NanoBanana - Cloud Run Deployment Script
# Simple one-command deployment!

set -e  # Exit on error

# Configuration
PROJECT_ID="your-gcp-project-id"  # Change this!
SERVICE_NAME="nanobanana"
REGION="us-central1"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "🍌 NanoBanana - Cloud Run Deployment"
echo "====================================="
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo "✓ gcloud CLI found"

# Check if GOOGLE_API_KEY is set
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "⚠️  GOOGLE_API_KEY not set in environment"
    echo "   Make sure to set it as a Cloud Run secret after deployment"
fi

# Build container
echo ""
echo "📦 Building Docker container..."
gcloud builds submit --tag ${IMAGE_NAME}

echo "✓ Container built: ${IMAGE_NAME}"

# Deploy to Cloud Run
echo ""
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --set-env-vars "GOOGLE_API_KEY=${GOOGLE_API_KEY}" \
    --memory 512Mi \
    --cpu 1 \
    --timeout 60 \
    --max-instances 10

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Service URL:"
gcloud run services describe ${SERVICE_NAME} --region ${REGION} --format 'value(status.url)'
echo ""
echo "📖 Test with:"
echo "curl -X POST \$(gcloud run services describe ${SERVICE_NAME} --region ${REGION} --format 'value(status.url)')/generate \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"prompt\": \"headshot of a CEO\"}'"
