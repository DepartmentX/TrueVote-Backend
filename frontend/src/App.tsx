import React from 'react';
import { RobotProvider } from './robocontext';
import Home from './home'

import ValidateVote from './ValidateVote';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

const App = () => (
  <RobotProvider>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/validateVote" element={<ValidateVote />} />
      </Routes>
    </BrowserRouter>
  </RobotProvider>
);

export default App;
