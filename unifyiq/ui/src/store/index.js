import { configureStore } from '@reduxjs/toolkit';
import userReducer from './userReducer';
import { connectorReducer } from './connectorReducer';

const store = configureStore({
    reducer: {
        user: userReducer, 
        connectors: connectorReducer
    }
})

export default store;
