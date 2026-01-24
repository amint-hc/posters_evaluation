# Academic Poster Evaluation System

**Graduation Project by:** Mahmoud Masri & Hala Hamood  
**Institution:** Tel Aviv University

## Project Overview

This is an AI-powered academic poster evaluation system that automatically analyzes and grades academic poster using OpenAI's GPT-4 Vision API. The system evaluates posters against a comprehensive 16-question rubric across 5 categories and provides detailed feedback.

### Academic Context

This system was developed as a graduation project to automate the evaluation of academic poster using AI. It demonstrates:
- Integration of AI vision models for academic assessment
- Development of user-friendly interfaces for non-technical users
- Implementation of multiple evaluation strategies for comprehensive analysis
- Generation of academic-ready reports and comparisons

### Key Features

- **Automated Evaluation:** Uses AI to evaluate posters based on academic criteria
- **Multiple Approaches:** Runs 4 different evaluation strategies for comprehensive comparison:
  - **Direct:** Fast evaluation with immediate grading
  - **Reasoning:** Detailed explanations for each score
  - **Deep Analysis:** Two-phase evaluation with evidence collection
  - **Strict:** Conservative scoring with strict criteria
- **User-Friendly GUI:** Simple interface requiring no technical knowledge
- **Excel Export:** Generates formatted Excel files with comparison tables
- **Batch Processing:** Evaluate multiple posters simultaneously

### Project Screenshot

![Project Screenshot](docs/project.png)

## File Structure

```
posters_evaluation/
├── gui/                    # GUI application module
│   ├── __init__.py         # Package initialization
│   ├── app.py              # Main GUI application window
│   └── backend.py          # Backend logic (server management, API communication)
├── src/                    # FastAPI backend source code
│   ├── main.py             # API endpoints and routes
│   ├── evaluator.py        # Evaluation engine and orchestration
│   ├── strategies.py       # Evaluation strategy implementations
│   ├── models/             # Data models and schemas
│   ├── processors/         # Output generators (Excel, reports)
│   ├── utils/              # Utility functions
│   └── exceptions.py       # Custom exceptions
├── run.py                  # Main entry point (starts server + GUI)
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── .env                    # Environment configuration (optional, gitignored)
├── .secret                 # API key storage (auto-created, gitignored, 7-day expiration)
├── bin/                    # Verification and utility scripts
├── uploads/                # Temporary poster storage (auto-created)
├── downloads/              # Generated evaluation results (auto-created)
└── docs/                   # Documentation and rubric details
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API Key (sign up at [OpenAI](https://platform.openai.com/signup) if you don't have one).
- Git (for cloning the repository)
- A folder containing the academic poster images (JPG, JPEG, PNG formats)

### Installation

Follow these steps to install and set up the system:

#### Step 1: Clone the Repository

If you haven't already, clone the repository to your local machine:

```bash
git clone https://github.com/amint-hc/posters_evaluation.git
cd posters_evaluation
```

If you already have the code, pull the latest changes:

```bash
git pull
```

#### Step 2: Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Setup Environment Configuration

1. Copy the example environment file:
   
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file with your configuration:
   
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   APP_PORT=8080
   ```
   
   You can set the key in `.env` OR enter it in the GUI (GUI method is recommended).

#### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- FastAPI (web framework)
- OpenAI (AI integration)
- Pandas & openpyxl (Excel generation)
- Tkinter (GUI - usually pre-installed with Python)

#### Step 5: Running the Application

```bash
python run.py
```

This command:
- Starts the FastAPI server (`http://localhost:8080`) in the background
- Launches the GUI application automatically: **"Academic Poster Evaluation System"** UI.
- Sets up all necessary components

#### Step 6: Using the GUI

1. **OpenAI API Key Management:**
   - On first run, the GUI will prompt you to enter your OpenAI API key
   - Paste your API key in the "OpenAI API Key" field
   - The key will be saved securely in a `.secret` file in your project directory
   - The saved key remains valid for 7 days
   - Use the "Show" checkbox to verify your key is correct
   - After 7 days, you'll need to re-enter it for security

2. **Select Posters Folder:**
   - Click the "Browse..." button
   - Navigate to the folder containing your poster images
   - Supported formats: JPG, JPEG, PNG
   - Select the folder and click "Select Folder"

3. **Run Evaluation:**
   - Click the "Evaluate Posters" button
   - The system will:
     - Verify the FastAPI server is running (starts automatically if needed)
     - Upload all posters from the selected folder to the server
     - Run all 4 evaluation approaches sequentially
     - Display progress in real-time with status updates

4. **View Results:**
   - Results will appear in the results table showing:
     - Project Number
     - Publisher Names
     - Grades from all 4 approaches (Direct, Reasoning, Deep Analysis, Strict)
   - Each row represents one evaluated poster

5. **Download Excel File:**
   - Click "Download Excel Results" after evaluation completes
   - Choose where to save the file on your computer
   - The Excel file contains a formatted comparison table with all results

### Testing

You can run GUI with mock data for testing without an OpenAI API key:

1. **Run the mock application:**
   
   ```bash
   python -m mock.app
   ```

2. **Use the GUI as normal:**  
   - Select a folder with sample posters (`mock/posters/`)
   - Run evaluation (mock data will be used)
   - Download results


### Understanding the Results

#### Grading Scale (0-100 points)

The system evaluates posters across 5 categories:

1. **Content Quality (25 points):**
   - Introduction clarity and structure
   - Topic alignment
   - Objective communication
   - Content relevance

2. **Research & Understanding (20 points):**
   - Topic understanding
   - References quality
   - Methodology clarity

3. **Visual Quality & Graphs (15 points):**
   - Graph readability
   - Visual relevance
   - Layout coherence

4. **Structure & Logical Flow (25 points):**
   - Section linkage
   - Logical connections
   - Internal consistency
   - Added value

5. **Results & Conclusions (15 points):**
   - Evidence support
   - Results clarity

#### Approach Comparison

- **Direct:** Fastest, good for initial assessment
- **Reasoning:** Best for understanding evaluation rationale
- **Deep Analysis:** Most thorough, best for research purposes
- **Strict:** Most conservative, useful for minimum standards
