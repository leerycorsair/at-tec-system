import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { API_URL, getHeaders, LOAD_STATUSES, MOCKING } from "../../GLOBAL";

export const loadModels = createAsyncThunk("models/load", async () => {
    const url = `${API_URL}/api/models/`;
    const headers = getHeaders();

    if (MOCKING) {
        console.log(url, {
            headers,
        });
        const json = {
            models: [
                {
                    id: 1,
                    name: "Модель 1",
                    created_at: "2024-09-29T09:11:24.520Z",
                },
            ],
            total: 0,
        };
        return json.models;
    }

    const response = await fetch(url, {
        headers,
    });
    const json = await response.json();
    return json.models;
});

export const createModel = createAsyncThunk("models/create", async (model) => {
    const url = `${API_URL}/api/models/`;
    const headers = getHeaders();
    if (MOCKING) {
        const json = model;
        if (!json.id) {
            json.id = Math.floor(Math.random() * 10000) + 1; // Generate random ID for new models
        }
        return json;
    }
    const response = await fetch(url, {
        method: "POST",
        headers,
        body: JSON.stringify(model),
    });
    const json = await response.json();
    return json;
});

export const deleteModel = createAsyncThunk("models/delete", async (modelId) => {
    const url = `${API_URL}/api/models/${modelId}/`;
    const headers = getHeaders();
    
    if (MOCKING) {
        console.log(url, {
            method: "DELETE",
            headers,
        });
        const json = { id: modelId };
        return json.id;
    }

    const response = await fetch(url, {
        method: "DELETE",
        headers,
    });
    const json = await response.json();
    return json;
});

const modelsSlice = createSlice({
    name: "models",
    initialState: {
        data: [],
        status: LOAD_STATUSES.IDLE,
        error: null,
    },
    reducers: {
        // Define reducers here
    },
    extraReducers: (builder) => {
        builder
            .addCase(loadModels.pending, (state) => {
                state.status = LOAD_STATUSES.LOADING;
            })
            .addCase(loadModels.fulfilled, (state, action) => {
                state.status = LOAD_STATUSES.SUCCESS;
                state.data = action.payload;
            })
            .addCase(createModel.pending, (state) => {
                state.status = LOAD_STATUSES.LOADING;
            })
            .addCase(createModel.fulfilled, (state, action) => {
                state.status = LOAD_STATUSES.SUCCESS;
                state.data.push(action.payload);
            })
            .addCase(deleteModel.pending, (state) => {
                state.status = LOAD_STATUSES.LOADING;
            })
            .addCase(deleteModel.fulfilled, (state, action) => {
                state.status = LOAD_STATUSES.SUCCESS;
                const index = state.data.findIndex((rt) => rt.id === action.payload);
                if (index > -1) {
                    state.data.splice(index, 1);
                }
            });
    },
});

export default modelsSlice.reducer;
