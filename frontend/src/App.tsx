import React from 'react';
import { RobotProvider } from './robocontext';
import Home from './home'

const App = () => (
  <RobotProvider>
    <Home />
  </RobotProvider>
);

export default App;
