import React, { useState } from 'react';
import { sha256 } from 'crypto-js/sha256'
import {
  Avatar,
  Button,
  Container,
  Grid,
  InputAdornment,
  TextField,
  Typography
} from '@material-ui/core';

import {
  LockOutlined,
  PersonOutlined,
  VpnKeyOutlined
} from '@material-ui/icons';

import useStyles from '../Style';
import axios from 'axios';

export default function Login(props) {

  document.title = 'Sentinel|LogIn';

  const classes = useStyles();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    portal: ''
  });

  function handleFormChange(event) {
    const { name, value } = event.target;
    setFormData(oldData => ({
      ...oldData,
      [name]: value
    }));
  };

  function handleFormSubmit(event) {
    // done to prevent any accidental revelation of passwords
    
    // formData.password = sha256(formData.password).toString();
    axios
      .post('http://localhost:5000/authenticate', formData)
      .then(res =>
        {
          console.log(res);
          if (res.data.status == 'Failed'){
            alert(res.data.log);
          }
          else if (res.data.url){
            alert('This site will redirect');
            window.location.href = res.data.url;
          }
      })
      .catch(err => {
        console.error(err);
        if (err.response) {
          alert('Your credentials are wrong!');
        }
        else {
          alert('There was some problem authenticating with the server.\n\nTry again later!');
        }
      })

    event.preventDefault();
  };

  return (
    <div className='LogIn'>
      <Container component='main' maxWidth='sm'>
        <div className={classes.paper}>
          <Avatar className={classes.avatar}>
            <LockOutlined />
          </Avatar>

          <Typography component='h1' variant='h5'>
            LogIn
          </Typography>

          <form className={classes.form} onSubmit={handleFormSubmit}>

            <Grid container spacing={4}>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  autoFocus
                  type='text'
                  variant='outlined'
                  label='Username'
                  name='username'
                  autoComplete='username'
                  value={formData.username}
                  onChange={handleFormChange}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position='start'>
                        <PersonOutlined />
                      </InputAdornment>
                    )
                  }}
                />
              </Grid>

              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  type='password'
                  variant='outlined'
                  label='Password'
                  name='password'
                  autoComplete='current-password'
                  value={formData.password}
                  onChange={handleFormChange}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position='start'>
                        <VpnKeyOutlined />
                      </InputAdornment>
                    )
                  }}
                />
              </Grid>

              <Grid item xs={12}>
                <Button
                  fullWidth
                  type='submit'
                  variant='contained'
                  color='primary'
                  className={classes.submit}
                >Log In</Button>
              </Grid>

            </Grid>

          </form>

        </div>
      </Container>
    </div>
  );
};
