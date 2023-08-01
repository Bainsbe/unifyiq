import {
  createSlice,
  createAsyncThunk,
  createEntityAdapter
} from '@reduxjs/toolkit';


const sessionAdapter = createEntityAdapter();

const initialState = sessionAdapter.getInitialState({
    session: [], 
    loading: false
})

const setAuthToken = (token) => {
  if (token) {
    localStorage.setItem('token', token);
  } else {
    localStorage.removeItem('token');
  }
};


export const verifiedEmail = createAsyncThunk('session/verifiedEmail', async (email, { dispatch,rejectWithValue }) => {
    try {
        const response = await fetch('/api/v1/auth/verified_email', {
          method: 'POST',
          headers: {
          'Content-Type': 'application/json',             
          },
          body: JSON.stringify({email})
        })
        if (response.ok) {
          const data = await response.json();
          dispatch(requestOTP(email))
          return data;
        } else {
          const data = await response.json(); 
          return data
        }
    } catch (err) {
      return rejectWithValue(err)
    }
    
} )

export const requestOTP = createAsyncThunk('session/requestOTP', async (email, {rejectWithValue}) => {
    try {
      const response = await fetch('/api/v1/auth/send_otp', {
        method: 'POST', 
        headers: {
          'Content-Type': 'application/json',             
        },
        body: JSON.stringify({email})
      })
      if (response.ok) {

      }
    }
    catch (err) {
      return rejectWithValue(err.error);
    }
})

export const login = createAsyncThunk('session/login', async ({ email, otp, time }, { rejectWithValue }) => {
    try {
      const response = await fetch('/api/v1/auth/login', {
        method: 'POST', 
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({email, otp, time})
      })
      if (response.ok) {
        const data = await response.json();
        setAuthToken(data.token);
        return data;
      } else {
        const err = await response.json();
        return err;
      }
    }
    catch(err) {
      return rejectWithValue(err.error);
    }
})

export const logout = createAsyncThunk('session/logout', async () => {
  try {
    const response = await fetch('/api/v1/auth/logout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', 
        'Authorization': `Bearer ${localStorage.getItem('Token')}`
      }
    })
    if (response.ok) {
      const data = await response.json();
      setAuthToken(data.token);
      return data;
    } else {
      const err = await response.json();
      return err;
    }
  }
  catch (err) {

  }
})

const sessionSlice = createSlice({
  name: 'sessions', 
  initialState, 
  reducers: {},
  extraReducers: {
    [verifiedEmail.pending]: (state) => {
      state.loading = true;
    }, 
    [verifiedEmail.fulfilled]: (state, {payload}) => {
      state.loading = false;
      state.session = payload;
    },
    [verifiedEmail.rejected]: (state) => {
      state.loading = false;
    }, 
    [login.pending]: (state) => {
      state.loading = true
    }, 
    [login.fulfilled]: (state, { payload }) => {
      state.loading = false;
      state.session = payload;
    }, 
    [login.rejected]: (state) => {
      state.loading = false;
    }, 
    [logout.pending]: (state) => {
      state.loading = true
    }, 
    [logout.fulfilled]: (state, { payload }) => {
      state.loading = false;
      state.session = payload;
    }, 
    [logout.rejected]: (state) => {
      state.loading = false;
    }, 
  }
})

export const sessionReducer = sessionSlice.reducer;
