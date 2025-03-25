"use client";

import { useState, useEffect, useRef } from "react";
import Head from "next/head";

export default function PomodoroTracker() {
  // Timer states
  const [minutes, setMinutes] = useState(25);
  const [seconds, setSeconds] = useState(0);
  const [isActive, setIsActive] = useState(false);
  const [isWorkSession, setIsWorkSession] = useState(true);
  const [sessionCount, setSessionCount] = useState(0);

  // Settings states
  const [workDuration, setWorkDuration] = useState(25);
  const [breakDuration, setBreakDuration] = useState(5);
  const [showSettings, setShowSettings] = useState(false);

  const timerRef = useRef(null);

  // Format time to display as MM:SS
  const formatTime = () => {
    return `${minutes.toString().padStart(2, "0")}:${seconds
      .toString()
      .padStart(2, "0")}`;
  };

  // Handle timer tick
  useEffect(() => {
    if (isActive) {
      timerRef.current = setInterval(() => {
        if (seconds === 0) {
          if (minutes === 0) {
            // Timer completed
            clearInterval(timerRef.current);
            playAlarm();
            switchSession();
          } else {
            setMinutes(minutes - 1);
            setSeconds(59);
          }
        } else {
          setSeconds(seconds - 1);
        }
      }, 1000);
    } else {
      clearInterval(timerRef.current);
    }

    return () => clearInterval(timerRef.current);
  }, [isActive, minutes, seconds]);

  // Play alarm sound when timer completes
  const playAlarm = () => {
    const audio = new Audio("/alarm.mp3"); // You would need to add this file
    audio.play().catch((e) => console.log("Audio play failed:", e));
  };

  // Switch between work and break sessions
  const switchSession = () => {
    setIsActive(false);
    if (isWorkSession) {
      // Switch to break
      setMinutes(breakDuration);
      setSessionCount(sessionCount + 1);
    } else {
      // Switch to work
      setMinutes(workDuration);
    }
    setSeconds(0);
    setIsWorkSession(!isWorkSession);
  };

  // Start timer
  const startTimer = () => {
    setIsActive(true);
  };

  // Pause timer
  const pauseTimer = () => {
    setIsActive(false);
  };

  // Reset timer to current session type
  const resetTimer = () => {
    setIsActive(false);
    setMinutes(isWorkSession ? workDuration : breakDuration);
    setSeconds(0);
  };

  // Apply custom durations
  const applySettings = () => {
    setMinutes(isWorkSession ? workDuration : breakDuration);
    setSeconds(0);
    setShowSettings(false);
  };

  // Timer progress for circular progress bar
  const progress = () => {
    const totalSeconds = (isWorkSession ? workDuration : breakDuration) * 60;
    const remainingSeconds = minutes * 60 + seconds;
    return ((totalSeconds - remainingSeconds) / totalSeconds) * 100;
  };

  return (
    <div className="min-h-screen bg-blue-50 flex flex-col items-center justify-center p-4">
      <Head>
        <title>Pomodoro Tracker</title>
        <meta name="description" content="A simple Pomodoro timer" />
      </Head>

      <main className="w-full max-w-md bg-white rounded-2xl shadow-xl overflow-hidden">
        {/* Header */}
        <div className="bg-blue-600 p-6 text-white text-center">
          <h1 className="text-3xl font-bold">Pomodoro Tracker</h1>
          <p className="mt-2 opacity-90">
            {isWorkSession ? "Focus Time" : "Break Time"} | Session:{" "}
            {sessionCount}
          </p>
        </div>

        {/* Timer Display */}
        <div className="p-8 flex flex-col items-center">
          {/* Circular progress bar */}
          <div className="relative w-64 h-64 mb-8">
            <svg className="w-full h-full" viewBox="0 0 100 100">
              {/* Background circle */}
              <circle
                cx="50"
                cy="50"
                r="45"
                fill="none"
                stroke="#EFF6FF"
                strokeWidth="8"
              />
              {/* Progress circle */}
              <circle
                cx="50"
                cy="50"
                r="45"
                fill="none"
                stroke="#3B82F6"
                strokeWidth="8"
                strokeDasharray="283"
                strokeDashoffset={283 - (283 * progress()) / 100}
                strokeLinecap="round"
                transform="rotate(-90 50 50)"
              />
            </svg>
            {/* Timer text */}
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-5xl font-bold text-blue-800">
                {formatTime()}
              </span>
            </div>
          </div>

          {/* Timer Controls */}
          <div className="flex space-x-4 mb-6">
            {!isActive ? (
              <button
                onClick={startTimer}
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-full font-medium text-lg shadow-md transition-colors"
              >
                Start
              </button>
            ) : (
              <button
                onClick={pauseTimer}
                className="bg-yellow-500 hover:bg-yellow-600 text-white px-6 py-3 rounded-full font-medium text-lg shadow-md transition-colors"
              >
                Pause
              </button>
            )}
            <button
              onClick={resetTimer}
              className="bg-blue-100 hover:bg-blue-200 text-blue-800 px-6 py-3 rounded-full font-medium text-lg shadow-md transition-colors"
            >
              Reset
            </button>
          </div>

          {/* Session Info */}
          <div className="text-center mb-6">
            <p className="text-blue-800 font-medium">
              Next: {isWorkSession ? "Break" : "Work"} Session
            </p>
            <p className="text-blue-600">
              {isWorkSession ? `${breakDuration} min` : `${workDuration} min`}
            </p>
          </div>

          {/* Settings Button */}
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="text-blue-600 hover:text-blue-800 font-medium flex items-center"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5 mr-1"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z"
                clipRule="evenodd"
              />
            </svg>
            Settings
          </button>
        </div>

        {/* Settings Panel */}
        {showSettings && (
          <div className="bg-blue-50 p-6 border-t border-blue-200">
            <h2 className="text-xl font-bold text-blue-800 mb-4">
              Timer Settings
            </h2>

            <div className="space-y-4">
              <div>
                <label className="block text-blue-700 mb-1">
                  Work Duration (minutes)
                </label>
                <input
                  type="number"
                  min="1"
                  max="60"
                  value={workDuration}
                  onChange={(e) =>
                    setWorkDuration(parseInt(e.target.value) || 1)
                  }
                  className="w-full p-2 text-blue-700 border border-blue-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-blue-700 mb-1">
                  Break Duration (minutes)
                </label>
                <input
                  type="number"
                  min="1"
                  max="60"
                  value={breakDuration}
                  onChange={(e) =>
                    setBreakDuration(parseInt(e.target.value) || 1)
                  }
                  className="w-full p-2 border text-blue-700  border-blue-300 rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div className="flex justify-end space-x-3 pt-2">
                <button
                  onClick={() => setShowSettings(false)}
                  className="px-4 py-2 text-blue-700 hover:text-blue-900 font-medium"
                >
                  Cancel
                </button>
                <button
                  onClick={applySettings}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded font-medium"
                >
                  Apply
                </button>
              </div>
            </div>
          </div>
        )}
      </main>

      <footer className="mt-8 text-center text-blue-600 text-sm">
        <p>
          Pomodoro Technique: 25 minutes of work followed by a 5-minute break
        </p>
      </footer>
    </div>
  );
}
