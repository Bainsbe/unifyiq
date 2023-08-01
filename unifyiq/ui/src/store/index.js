import { configureStore } from '@reduxjs/toolkit';
import { connectorReducer } from './connectorReducer';
import {sessionReducer} from './sessionReducer'

const store = configureStore({
    reducer: {
        session: sessionReducer, 
        connectors: connectorReducer
    }
})

export default store;
