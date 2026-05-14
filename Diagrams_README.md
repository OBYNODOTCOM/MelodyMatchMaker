# MelodyMatchMaker Architecture Diagrams

This folder contains three architectural diagrams for the MelodyMatchMaker music recommendation system:

## 📁 Files

### 1. `MelodyMatchMaker_Architecture.mmd`
**Comprehensive System Architecture**
- Shows the full stack from data sources through deployment
- Highlights all architectural layers and components
- Includes deployment options and external services

### 2. `MelodyMatchMaker_Flow.mmd`
**Recommendation Flow Diagram**
- Focuses on the user experience and recommendation pipeline
- Shows the complete user journey from search to playback
- Emphasizes the data preprocessing and recommendation logic

### 3. `MelodyMatchMaker_Technical.mmd`
**Technical Flow & Performance**
- State diagram showing system states and transitions
- Includes performance metrics and algorithm details
- Technical specifications for indexing and scoring

## 🔧 How to View

### Option 1: Online Mermaid Editor
1. Copy the content of any `.mmd` file
2. Go to https://mermaid.live/
3. Paste the content and click "Render"

### Option 2: VS Code Extension
1. Install the "Mermaid Preview" or "Markdown Preview Mermaid Support" extension
2. Open the `.mmd` file in VS Code
3. Use the preview feature to render the diagram

### Option 3: Export as Image
1. Use the online editor (Option 1)
2. Click "Download" to export as PNG/SVG

## 📊 Diagram Contents

- **Data Sources**: CSV files with Spotify track data
- **Processing Layer**: Data cleaning and feature extraction
- **Indexing Layer**: Ball Tree construction for fast similarity search
- **Recommendation Engine**: Hybrid scoring algorithm
- **UI Layer**: Search interface and Spotify embeds
- **Performance**: Sub-0.5s query times with ~4,831 tracks

## 🎯 Key Features Illustrated

- Precomputed indexing for instant recommendations
- Hybrid similarity + popularity scoring
- Spotify integration for interactive previews
- Scalable architecture for cloud deployment