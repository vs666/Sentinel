import React, { useState } from 'react';

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

import useStyles from './LoginStyle';

export default function Login(props) {

  document.title = 'Sentinel|LogIn';

  const classes = useStyles();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    portal: ''
  });

  function handleFormChange(event){
    const {name, value} = event.target;
    setFormData(oldData => ({
      ...oldData,
      [name]: value
    }));
  };

  function handleFormSubmit(event){
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
