#!/usr/bin/env python
"""
SmartFarmAI Frontend Configuration
Sets up proper CORS headers for connecting to Vercel-hosted frontend with Render-hosted backend
"""
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://*.vercel.app"  # Vercel preview & production domains
]

# Frontend URLs for development and production
FRONTEND_DEV_URL = "http://localhost:3000"
FRONTEND_PROD_URL = "https://your-frontend.vercel.app"  # Update with your Vercel URL
