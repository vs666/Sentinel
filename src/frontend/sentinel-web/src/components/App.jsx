import React from 'react';

import  {
  createTheme,
  ThemeProvider
} from '@material-ui/core/styles';

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
    <div className="App">
      <ThemeProvider theme={theme}>
        <h1>Welcomet to Sentinel</h1>
      </ThemeProvider>
    </div>
  );
}

export default App;
