# 💪 Juggernaut Training Program Generator

A beautiful Streamlit web application for generating personalized Juggernaut Method strength training programs.

## Features

- **Flexible Input**: Enter your 1RM directly or calculate it from weight × reps
- **Complete 16-Week Program**: All four waves (10s, 8s, 5s, 3s) with detailed progressions
- **Beautiful UI**: Modern, responsive interface with organized data tables
- **CSV Export**: Download your complete program for offline use
- **Real-time Calculations**: Instant program generation based on your maxes

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the App

Run the Streamlit app with:
```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## How to Use

1. **Choose Input Method**:
   - **Direct 1RM**: Enter your known 1 rep max for each lift
   - **Calculate from Weight x Reps**: Enter a weight and reps to estimate your 1RM

2. **Enter Your Lifts**:
   - Bench Press
   - Squat
   - Deadlift

3. **Generate Program**: Click the "Generate My Program" button

4. **View & Download**: 
   - Review your 16-week program organized by waves
   - Download as CSV for tracking in your gym

## About Juggernaut Method

The Juggernaut Method is a 16-week strength program divided into four 4-week waves:
- **10s Wave**: Build volume and work capacity
- **8s Wave**: Increase intensity while maintaining volume
- **5s Wave**: Focus on strength development
- **3s Wave**: Peak strength and power

Each wave includes 3 weeks of progressive overload followed by a deload week.

## Program Structure

- Week 1-2: Progressive loading
- Week 3: AMRAP (As Many Reps As Possible) sets
- Week 4: Deload week for recovery

---

*Train hard, train smart 💪*
