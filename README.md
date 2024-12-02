ZiWeiDouShu + MBTI Personal Growth Application
============================================

Project Structure
----------------

Frontend (/frontend):
- Main Application (App.tsx)
  * Profile collection (birth date/time, MBTI)
  * Base score system from ZiWeiDouShu analysis
  * Activity-enhanced scoring visualization
  * Interactive progress tracking with layered visualization
    - Base scores from ZiWeiDouShu
    - Activity bonus scores
    - Total combined scores
    - Potential maximum scores
  * Multiple visualization types:
    - Area charts for progress over time
    - Radar charts for aspect balance
    - Activity impact tracking

Backend (/backend):
- Main Components:
  * main.py - FastAPI endpoints & routing
  * integrator.py - System orchestration

- Processors:
  * ziwei_processor.py - Base score calculations
  * mbti_processor.py - Activity recommendations
  * combined_analyzer.py - Score integration system

- Tracking:
  * survey_manager.py 
    - Core aspect questions
    - Activity-specific questions (structure ready)
    - Response analysis
  * progress_tracker.py
    - Base score tracking
    - Activity bonus calculations
    - Progress snapshots

Key Features (Current Focus)
-----------
1. Layered Scoring System:
   - ZiWeiDouShu base calculations
   - Activity bonus integration
   - Combined score visualization

2. Progress Visualization:
   - Interactive aspect selection
   - Multi-layered area charts
   - Activity impact display

3. Survey System:
   - Core aspect reflection
   - Activity progress tracking
   - Weekly data collection

Setup Instructions
----------------
Frontend:
1. cd frontend
2. npm install
3. npm start
Access at http://localhost:3000

Backend:
1. conda activate ziweidoushu
2. cd backend
3. python -m uvicorn main:app --reload --port 8000
Access at http://localhost:8000

Current Development Status
------------------
- Core progress visualization implemented
- Survey system structure established
- Activity tracking integration in progress
- Base and bonus score calculation system ready

Note: Current focus is on refining the visualization of base scores from ZiWeiDouShu and their interaction with activity bonuses.