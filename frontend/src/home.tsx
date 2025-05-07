import React, { useState, useEffect } from 'react';
import ReCaptcha from './recaptcha';
import { useRobot } from './robocontext';
import './App.css';

function Home() {
  const { isRobot, setIsRobot } = useRobot(); // Access robot context
  const [verifiedToken, setVerifiedToken] = useState<string | null>(null);
  const [lockedOut, setLockedOut] = useState<boolean>(false);

  const handleVerify = (token: string | null) => {
    setVerifiedToken(token);
  };

  const handleLock = () => {
    setLockedOut(true); // 😬 user hit max attempts
    setIsRobot(1); // Set robot detected flag
  };

  const handleSubmit = async () => {
    if (lockedOut) {
      alert('You cannot submit anymore. You have reached the maximum number of CAPTCHA attempts.');
      return;
    }

    if (!verifiedToken) {
      alert('Please complete the reCAPTCHA');
      return;
    }

    const response = await fetch('http://localhost:8000/verify-captcha', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token: verifiedToken }),
    });

    const data = await response.json();
    if (data.success) {
      alert('CAPTCHA verified!');
      window.location.href = '/validateVote'; // Navigate to validateVote.tsx
    } else {
      alert('CAPTCHA failed!');
    }
  };

  return (
    <div className="App">
      <h1>reCAPTCHA Demo</h1>
      <ReCaptcha onVerify={handleVerify} onLock={handleLock} />
      <br />
      <button onClick={handleSubmit} disabled={lockedOut}>Submit</button>
      {isRobot === 1 && <p style={{ color: 'red' }}></p>}
    </div>
  );
}

export default Home;