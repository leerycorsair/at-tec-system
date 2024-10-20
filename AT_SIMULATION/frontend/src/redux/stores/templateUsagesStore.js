import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { createFrameActionAsyncThunk } from "../frameActor";
import { API_URL, getHeaders, LOAD_STATUSES, MOCKING } from "../../GLOBAL";

export const loadTemplateUsages = createAsyncThunk("templateUsages/load", async (modelId) => {
    const url = `${API_URL}/api/editor/templates/usages/`;
    const headers = getHeaders({ "model-id": modelId });

    if (MOCKING) {
        console.log(url, {
            headers,
        });
        const json = {
            usages: [
                {
                    id: 1,
                    name: "usage1",
                    template_id: 1,
                    arguments: [
                        {
                            id: 1,
                            relevant_resource_id: 1,
                            resource_id: 1,
                        },
                    ],
                },
            ],
            total: 0,
        };
        return { items: json.usages, modelId };
    }

    const response = await fetch(url, {
        headers,
    });
    const json = await response.json();
    return { items: json.usages, modelId };
});

export const createTemplateUsage = createFrameActionAsyncThunk("templateUsages/create", async ({ modelId, templateUsage }) => {
    const url = `${API_URL}/api/editor/templates/usages/`;
    const headers = getHeaders({ "model-id": modelId });

    if (MOCKING) {
        console.log(url, {
            method: "POST",
            headers,
            body: JSON.stringify(templateUsage),
        });
        const json = templateUsage;

        if (!json.id) {
            json.id = Math.floor(Math.random() * 10000) + 1;
        }
        return json;
    }
    const response = await fetch(url, {
        method: "POST",
        headers,
        body: JSON.stringify(templateUsage),
    });
    const json = await response.json();
    return json;
});

export const updateTemplateUsage = createFrameActionAsyncThunk("templateUsages/update", async ({ modelId, templateUsage }) => {
    const url = `${API_URL}/api/editor/templates/usages/${templateUsage.id}/`;
    const headers = getHeaders({ "model-id": modelId });

    if (MOCKING) {
        console.log(url, {
            method: "PUT",
            headers,
            body: JSON.stringify(templateUsage),
        });
        const json = templateUsage;
        return json;
    }

    const response = await fetch(url, {
        method: "PUT",
        headers,
        body: JSON.stringify(templateUsage),
    });
    const json = await response.json();
    return json;
});

export const deleteTemplateUsage = createFrameActionAsyncThunk("templateUsages/delete", async ({ modelId, templateUsageId }) => {
    const url = `${API_URL}/api/editor/templates/usages/${templateUsageId}/`;
    const headers = getHeaders({ "model-id": modelId });

    if (MOCKING) {
        console.log(url, {
            method: "DELETE",
            headers,
        });
        const json = { id: templateUsageId };
        return json.id;
    }

    const response = await fetch(url, {
        method: "DELETE",
        headers,
    });
    const json = await response.json();
    return json.id;
});

const templateUsagesSlice = createSlice({
    name: "templateUsages",
    initialState: {
        data: [],
        status: LOAD_STATUSES.IDLE,
        error: null,
        modelId: null,
    },
    reducers: {
        // Define reducers here
    },
    extraReducers: (builder) => {
        builder
            .addCase(loadTemplateUsages.pending, (state) => {
                state.status = LOAD_STATUSES.LOADING;
            })
            .addCase(loadTemplateUsages.fulfilled, (state, action) => {
                state.status = LOAD_STATUSES.SUCCESS;
                state.data = action.payload.items;
                state.modelId = action.payload.modelId;
            })
            .addCase(createTemplateUsage.pending, (state) => {
                state.status = LOAD_STATUSES.LOADING;
            })
            .addCase(createTemplateUsage.fulfilled, (state, action) => {
                state.status = LOAD_STATUSES.SUCCESS;
                state.data.push(action.payload);
            })
            .addCase(updateTemplateUsage.pending, (state) => {
                state.status = LOAD_STATUSES.LOADING;
            })
            .addCase(updateTemplateUsage.fulfilled, (state, action) => {
                state.status = LOAD_STATUSES.SUCCESS;
                const index = state.data.findIndex((item) => item.id === action.payload.id);
                if (index > -1) {
                    state.data[index] = action.payload;
                }
            })
            .addCase(deleteTemplateUsage.pending, (state) => {
                state.status = LOAD_STATUSES.LOADING;
            })
            .addCase(deleteTemplateUsage.fulfilled, (state, action) => {
                state.status = LOAD_STATUSES.SUCCESS;
                const index = state.data.findIndex((item) => item.id === action.payload);
                if (index > -1) {
                    state.data.splice(index, 1);
                }
            });
    },
});

export default templateUsagesSlice.reducer;
