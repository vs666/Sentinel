import React from 'react';

import  {
  createTheme,
  ThemeProvider
} from '@material-ui/core/styles';

import {
  BrowserRouter as Router,
  Route,
  Switch
} from 'react-router-dom';

import Login from './auth/login/Login';
import Register from './auth/register/Register';

function App() {

  const theme = createTheme({
    typography: {
      fontFamily: [
        'JetBrains Mono',
        'monospace'
      ].join(',')
    },
    palette: {
      secondary: {
        main: '#3f51b5'
      }
    }
  });

  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Switch>

          <Route path='/' exact render={(props) => (
            <h1>Home Page</h1>
          )} />

          <Route path='/login' exact render={(props) => (
            <Login />
          )} />

          <Route path='/register' exact render={(props) => (
            <Register />
          )} />

        </Switch>
      </Router>
    </ThemeProvider>
  );
}

export default App;
