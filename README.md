# TDS Virtual TA
## A Test for the TDS Virtual TA Chatbot

### Step 1 : Installation
1. Install all requirements
`pip install requirements.txt`

2. Intall all requirements for scraping
`pip install requirements_scraping.txt`

3. Install all browsers for Playwright
`playwright install`

### Step 2 : Initialize API Key
1. Go to https://aipipe.org/
2. Login with your IITM student email
3. Navigate to your account settings or API section
4. Copy your API key and paste it in the .env file

### Step 3 : Scraping
1. Run `python course_scraper.py`
2. Run `python discourse_scraper.py`

### Step 4 : Pre-processing
1. Run `python preprocess.py`

### Step 5 : Vercel Hosting
1. Step 1 : Push to a new GitHub Repository
2. Step 2 : Add an MIT License to the repository
- To do this, go to GitHub, then to your repository
- Click "Add File"
- In the editor, enter "LICENSE" as the file name and a button will show up for the LICENSE Template.
- Select MIT License and click ok.
3. Step 3 : Connect to Vercel
- Sign up or log in to Vercel
- Click "Add New" → "Project"
- Connect your GitHub account if not already connected
- Find and select your repository from the list
4. Step 4 : Configure Environment Variables
- In the Vercel project setup page, click "Environment Variables"
- Add a new variable with name exactly as: API_KEY
- Paste your aipipe key as the value
- Ensure the variable is enabled for Production, Preview, and Development
- Click "Add" to save the variable
5. Step 5 : Deploy
- Click "Deploy" button and wait for deployment to complete
- Vercel will show "Your project has been deployed" when finished
- Click on the deployment URL to view your API

### Step 6 : Evaluation
1. Run `npx -y promptfoo eval --config project-tds-virtual-ta-promptfoo.yaml --no-cache`