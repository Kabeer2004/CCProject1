# Pomodoro Tracker - Next.js Application

![Pomodoro Timer App](https://github.com/user-attachments/assets/5fb55cb0-f738-471f-a6cb-282e2a4ade44)

A responsive Pomodoro timer application built with Next.js and Tailwind CSS, following the Pomodoro Technique for productivity.

## Features

### 🕒 Core Timer Functionality
- **25-minute work sessions** and **5-minute break sessions** by default
- **Visual countdown timer** with minutes and seconds display
- **Circular progress indicator** showing elapsed time
- **Automatic session switching** between work and break periods
- **Session counter** to track completed work sessions

### 🎛️ Timer Controls
- **Start/Pause button** to control the timer
- **Reset button** to restart the current session
- **Visual feedback** when timer completes (would include sound with proper audio file)

### ⚙️ Customizable Settings
- Adjustable **work duration** (1-60 minutes)
- Adjustable **break duration** (1-60 minutes)
- Settings panel that can be toggled on/off
- Instant application of new timer settings

### 🎨 UI/UX Features
- Clean, **responsive design** that works on all device sizes
- **Blue color palette** as requested
- Clear visual distinction between work and break modes
- Intuitive interface with minimal learning curve
- **Session information** showing current and next session type

## Technologies Used
- **Next.js** - React framework for building the application
- **Tailwind CSS** - Utility-first CSS framework for styling
- **React Hooks** (useState, useEffect, useRef) - For state management
- **SVG** - For the circular progress indicator

## Getting Started

### Prerequisites
- Node.js (v14 or later recommended)
- npm or yarn

### Installation
1. Clone the repository
   ```bash
   git clone https://github.com/your-username/pomodoro-tracker.git
   ```
2. Install dependencies
   ```bash
   cd pomodoro-tracker
   npm install
   # or
   yarn install
   ```
3. Run the development server
   ```bash
   npm run dev
   # or
   yarn dev
   ```
4. Open [http://localhost:3000](http://localhost:3000) in your browser

## How to Use
1. **Start the timer** by clicking the Start button
2. **Pause** if you need to take an unscheduled break
3. **Reset** to restart the current session
4. Click **Settings** to adjust work/break durations
   - Enter your preferred times
   - Click Apply to save changes

## Future Enhancements
- Add alarm sound when timer completes
- Implement long break after several work sessions
- Add task management functionality
- Dark mode toggle
- Save settings to localStorage

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
