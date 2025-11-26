# Trademark Awareness Survey Dashboard

Streamlit-based interactive dashboard for analyzing trademark awareness survey data from Vijayawada traders.

## Features

- 📊 Interactive data visualizations
- 📈 Multiple analysis tabs (Demographics, Business Profile, Trademark Awareness, etc.)
- 📤 CSV file upload support
- 🎨 Custom themed charts using Plotly

## Local Development

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   streamlit run streamlit_survey_dashboard.py
   ```

3. **Access the dashboard:**
   - Open your browser to `http://localhost:8501`

## Deployment to Streamlit Cloud (FREE)

### Step 1: Create GitHub Repository

1. Create a new GitHub repository (e.g., `survey-dashboard`)
2. Copy the `ravi_survey` folder contents to the repo
3. Make sure these files are in the root:
   - `streamlit_survey_dashboard.py`
   - `requirements.txt`
   - `ravi_survey.csv`
   - `.streamlit/config.toml`

### Step 2: Deploy to Streamlit Cloud

1. **Go to:** https://share.streamlit.io/
2. **Click:** "New app"
3. **Connect:** Your GitHub repository
4. **Configure:**
   - Repository: `your-username/survey-dashboard`
   - Branch: `main`
   - Main file path: `streamlit_survey_dashboard.py`
5. **Click:** "Deploy!"

### Step 3: Get Your App URL

After deployment (2-3 minutes), you'll get a URL like:
```
https://your-username-survey-dashboard.streamlit.app
```

### Step 4: Update Next.js Page

Copy the Streamlit URL and update in `/src/app/survey/page.tsx`:
```typescript
const STREAMLIT_URL = 'https://your-username-survey-dashboard.streamlit.app';
```

## File Structure

```
ravi_survey/
├── streamlit_survey_dashboard.py   # Main Streamlit app
├── ravi_survey.csv                 # Default survey data
├── ravi_survey_ori.csv             # Original data backup
├── ravi_survey_charts.py           # Additional chart utilities
├── requirements.txt                # Python dependencies
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
└── README.md                       # This file
```

## Data Format

The app expects a CSV file with the following column structure:
- Gender
- Age
- Education
- Business Type
- Business Years
- Trademark Knowledge
- Registration Status
- And more...

## Customization

### Theme Colors

Edit `.streamlit/config.toml` to change theme colors:
```toml
[theme]
primaryColor = "#3b82f6"        # Blue accent
backgroundColor = "#ffffff"      # White background
secondaryBackgroundColor = "#f1f5f9"  # Light gray
textColor = "#1e293b"           # Dark text
```

### Add More Charts

Add new visualizations in the tab sections of `streamlit_survey_dashboard.py`

## Integration with Main Website

The survey dashboard is embedded in the main Next.js website at `/survey` using an iframe.

**URL:** https://zadenor.com/survey

## Support

For issues or questions, contact: customer.care@zadenor.com

## License

© 2025 ZadeNor AI. All rights reserved.
