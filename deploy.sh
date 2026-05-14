#!/bin/bash

# MelodyMatchMaker Deployment Script

echo "🚀 MelodyMatchMaker Deployment Script"
echo "===================================="

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the project root."
    exit 1
fi

# Function to deploy to Streamlit Cloud
deploy_streamlit_cloud() {
    echo "📦 Deploying to Streamlit Cloud..."
    echo "1. Go to https://share.streamlit.io"
    echo "2. Connect your GitHub account"
    echo "3. Select this repository"
    echo "4. Set main file path to: app.py"
    echo "5. Click Deploy"
    echo ""
    echo "⚠️  Note: User data won't persist between deployments on Streamlit Cloud"
}

# Function to deploy to Heroku
deploy_heroku() {
    echo "🐘 Deploying to Heroku..."

    # Check if Heroku CLI is installed
    if ! command -v heroku &> /dev/null; then
        echo "❌ Heroku CLI not found. Please install from https://devcenter.heroku.com/articles/heroku-cli"
        exit 1
    fi

    # Check if git repo exists
    if [ ! -d ".git" ]; then
        echo "📝 Initializing git repository..."
        git init
        git add .
        git commit -m "Initial deployment"
    fi

    # Create Heroku app
    echo "🌟 Creating Heroku app..."
    heroku create melody-matchmaker --stack=container

    # Set buildpack for Python
    heroku buildpacks:set heroku/python

    # Deploy
    echo "🚀 Deploying to Heroku..."
    git push heroku main

    # Open app
    heroku open
}

# Function to deploy locally with Docker
deploy_docker() {
    echo "🐳 Deploying with Docker..."

    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker not found. Please install Docker first."
        exit 1
    fi

    echo "🏗️  Building Docker image..."
    docker build -t melody-matchmaker .

    echo "🚀 Running container..."
    docker run -d -p 8501:8501 --name melody-matchmaker-app melody-matchmaker

    echo "✅ App running at http://localhost:8501"
    echo "To stop: docker stop melody-matchmaker-app"
    echo "To remove: docker rm melody-matchmaker-app"
}

# Function to deploy with docker-compose
deploy_docker_compose() {
    echo "🐳 Deploying with Docker Compose..."

    if ! command -v docker-compose &> /dev/null && ! command -v docker &> /dev/null | grep -q "compose"; then
        echo "❌ Docker Compose not found."
        exit 1
    fi

    echo "🚀 Starting services..."
    docker-compose up -d

    echo "✅ App running at http://localhost:8501"
    echo "To stop: docker-compose down"
}

# Main menu
echo "Choose deployment method:"
echo "1. Streamlit Cloud (Free, Easy)"
echo "2. Heroku (Free tier available)"
echo "3. Docker (Local container)"
echo "4. Docker Compose (Local with volumes)"
echo "5. Local development"
echo ""

read -p "Enter choice (1-5): " choice

case $choice in
    1)
        deploy_streamlit_cloud
        ;;
    2)
        deploy_heroku
        ;;
    3)
        deploy_docker
        ;;
    4)
        deploy_docker_compose
        ;;
    5)
        echo "💻 Local development:"
        echo "Run: streamlit run app.py"
        echo "App will be available at http://localhost:8501"
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment complete!"
echo "📖 Check DEPLOYMENT.md for more details and troubleshooting."