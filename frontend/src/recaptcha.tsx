// src/components/ReCaptcha.tsx
import React, { useState, useEffect } from 'react';
import ReCAPTCHA from 'react-google-recaptcha';
import { useRobot } from './robocontext'; // 💥 bring in context

const SITE_KEY = '6LfaMTArAAAAALD2BVOI4ZP8MjcL_esx4_LBZhTT';

interface ReCaptchaProps {
  onVerify: (token: string | null) => void;
  onLock: () => void;
}

const ReCaptcha: React.FC<ReCaptchaProps> = ({ onVerify, onLock }) => {
  const [token, setToken] = useState<string | null>(null);
  const [attempts, setAttempts] = useState<number>(0);
  const { setIsRobot } = useRobot(); // 👈 use context
  const MAX_ATTEMPTS = 3;

  // Load attempts from localStorage
  useEffect(() => {
    const storedAttempts = localStorage.getItem('attempts');
    if (storedAttempts) {
      const parsed = parseInt(storedAttempts);
      setAttempts(parsed);
      if (parsed >= 1) {
        setIsRobot(1); // 💥 if already had failed attempts
      }
    }
  }, []);

  // Save attempts and update isRobot when changed
  useEffect(() => {
    localStorage.setItem('attempts', attempts.toString());
    if (attempts >= 1) {
      setIsRobot(1); // 💥 immediately set robot if 1+
    }
  }, [attempts]);

  const handleChange = (value: string | null) => {
    if (attempts >= MAX_ATTEMPTS) return;

    if (value) {
      setToken(value);
      onVerify(value);
    } else {
      const newAttempts = attempts + 1;
      setAttempts(newAttempts);
      onVerify(null);
      if (newAttempts >= MAX_ATTEMPTS) {
        onLock();
      }
    }
  };

  return (
    <div>
      {attempts >= MAX_ATTEMPTS ? (
        <p style={{ color: 'red' }}>You have reached the maximum number of attempts.</p>
      ) : (
        <ReCAPTCHA
          sitekey={SITE_KEY}
          onChange={handleChange}
          onExpired={() => handleChange(null)}
          onErrored={() => handleChange(null)}
          theme="light"
        />
      )}
    </div>
  );
};

export default ReCaptcha;
