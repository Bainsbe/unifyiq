import {
    createSlice,
    createAsyncThunk,
    createEntityAdapter
} from '@reduxjs/toolkit';

const connectorAdapter = createEntityAdapter();

const initialState = connectorAdapter.getInitialState({
    connectors: [],
    loading: false
})

export const listConnectors = createAsyncThunk('connector/listConnectors', async () => {
    const response = await fetch('/api/v1/connectors/list',)
    const data = await response.json();
    return data;
})

export const addConnectors = createAsyncThunk('connector/addConnectors', async (connectorInfo, {rejectWithValue}) => {
    const { name, url_prefix, connector_type, last_fetched_ts, start_ts, is_enabled, config_json } = connectorInfo;
    try {
        const response = await fetch('/api/v1/connectors/new', {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json',             
            },
            body: JSON.stringify({name, url_prefix, connector_type, last_fetched_ts, start_ts, is_enabled, config_json})
        })
        if (response.ok) {
            const data = await response.json();
            return data;
        } else {
            const err = await response.json();
            return err;
        }
    } catch (err) {
        return rejectWithValue(err.error);
    }
})


const connectorSlice = createSlice({
    name: 'connectors',
    initialState, 
    reducers: {
        
    },
    extraReducers: {
        [listConnectors.pending]: (state) => {
            state.loading = true;
        }, 
        [listConnectors.fulfilled]: (state, { payload }) => {
            state.loading = false; 
            state.connectors = payload; 
        }, 
        [listConnectors.rejected]: (state) => {
            state.loading = false;
        },
        [addConnectors.pending]: (state) => {
            state.loading = true;
        }, 
        [addConnectors.fulfilled]: (state, { payload }) => {
            state.loading = false; 
            state.connectors = payload;
        }, 
        [addConnectors.rejected]: (state) => {
            state.loading = false;
        }

    }
})


export const connectorReducer= connectorSlice.reducer;
