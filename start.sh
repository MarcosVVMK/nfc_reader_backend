#!/bin/bash

# Startup script for FastAPI Backend
echo "🚀 Starting Prog3 Backend with Docker Compose"

# Check if docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

# Check if docker compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
fi

echo "🏗️  Building and starting containers..."

# Use docker compose or docker-compose (depending on what's available)
if command -v docker-compose &> /dev/null; then
    docker-compose up --build
elif docker compose version &> /dev/null 2>&1; then
    docker compose up --build
else
    echo "❌ Neither 'docker-compose' nor 'docker compose' commands are available."
    exit 1
fi