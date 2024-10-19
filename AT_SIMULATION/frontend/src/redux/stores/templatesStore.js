import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { API_URL, getHeaders, LOAD_STATUSES, MOCKING } from "../../GLOBAL";

export const loadTemplates = createAsyncThunk("templates/load", async (modelId) => {
    const url = `${API_URL}/api/editor/templates/`;
    const headers = getHeaders({ "model-id": modelId });

    if (MOCKING) {
        console.log(url, {
            headers,
        });
        const json = {
            irregular_events: [
                {
                    meta: {
                        id: 1,
                        name: "event1",
                        type: "irregular_event",
                        rel_resources: [
                            {
                                id: 1,
                                name: "rel_res1",
                                resource_type_id: 1,
                            },
                        ],
                    },
                    generator: {
                        type: "normal",
                        value: 2,
                        dispersion: 0,
                    },
                    body: {
                        body: "rel_res1.attr1 = 5",
                    },
                },
            ],
            operations: [
                {
                    meta: {
                        id: 2,
                        name: "operation1",
                        type: "operation",
                        rel_resources: [
                            {
                                id: 1,
                                name: "rel_res1",
                                resource_type_id: 1,
                            },
                        ],
                    },
                    body: {
                        condition: "rel_res1.attr1 == 5",
                        body_before: "rel_res1.attr2 = 7",
                        delay: 3,
                        body_after: "rel_res1.attr3 = false",
                    },
                },
            ],
            rules: [
                {
                    meta: {
                        id: 3,
                        name: "rule1",
                        type: "rule",
                        rel_resources: [
                            {
                                id: 1,
                                name: "rel_res1",
                                resource_type_id: 1,
                            },
                        ],
                    },
                    body: {
                        condition: "rel_res1.attr1 == 5",
                        body: "rel_res1.attr2 = 7",
                    },
                },
            ],
        };
        return { items: json.irregular_events.concat(json.operations.concat(json.rules)), modelId };
    }

    const response = await fetch(url, {
        headers,
    });
    const json = await response.json();
    return { items: json.irregular_events.concat(json.operations.concat(json.rules)), modelId };
});

export const createTemplate = createAsyncThunk("templates/create", async ({ modelId, template }) => {
    const url = `${API_URL}/api/editor/templates/${template.meta.type}/`;
    const headers = getHeaders({ "model-id": modelId });
    if (MOCKING) {
        console.log(url, {
            method: "POST",
            headers,
            body: JSON.stringify(template),
        });
        const json = template;

        if (!json.meta.id) {
            json.meta.id = Math.floor(Math.random() * 10000) + 1;
        }
        return json;
    }

    const response = await fetch(url, {
        method: "POST",
        headers,
        body: JSON.stringify(template),
    });
    const json = await response.json();
    return json;
});

export const updateTemplate = createAsyncThunk("templates/update", async ({ modelId, template }) => {
    const url = `${API_URL}/api/editor/templates/${template.meta.id}/${template.meta.type}/`;
    const headers = getHeaders({ "model-id": modelId });

    if (MOCKING) {
        console.log(url, {
            method: "PUT",
            headers,
            body: JSON.stringify(template),
        });
        const json = template;
        return json;
    }

    const response = await fetch(url, {
        method: "PUT",
        headers,
        body: JSON.stringify(template),
    });
    const json = await response.json();
    return json;
});

export const deleteTemplate = createAsyncThunk("templates/delete", async ({ modelId, templateId }) => {
    const url = `${API_URL}/api/editor/templates/${templateId}/`;
    const headers = getHeaders({ "model-id": modelId });

    if (MOCKING) {
        console.log(url, {
            method: "DELETE",
            headers,
        });
        const json = { id: templateId };
        return json.id;
    }

    const response = await fetch(url, {
        method: "DELETE",
        headers,
    });
    const json = await response.json();
    return json.id;
});

const templatesSlice = createSlice({
    name: "templates",
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
            .addCase(loadTemplates.pending, (state) => {
                state.status = LOAD_STATUSES.LOADING;
            })
            .addCase(loadTemplates.fulfilled, (state, action) => {
                state.status = LOAD_STATUSES.SUCCESS;
                state.data = action.payload.items;
                state.modelId = action.payload.modelId;
            })
            .addCase(createTemplate.pending, (state) => {
                state.status = LOAD_STATUSES.LOADING;
            })
            .addCase(createTemplate.fulfilled, (state, action) => {
                state.status = LOAD_STATUSES.SUCCESS;
                state.data.push(action.payload);
            })
            .addCase(updateTemplate.pending, (state) => {
                state.status = LOAD_STATUSES.LOADING;
            })
            .addCase(updateTemplate.fulfilled, (state, action) => {
                state.status = LOAD_STATUSES.SUCCESS;
                const index = state.data.findIndex((item) => item.meta.id === action.payload.meta.id);
                if (index > -1) {
                    state.data[index] = action.payload;
                }
            })
            .addCase(deleteTemplate.pending, (state) => {
                state.status = LOAD_STATUSES.LOADING;
            })
            .addCase(deleteTemplate.fulfilled, (state, action) => {
                state.status = LOAD_STATUSES.SUCCESS;
                const index = state.data.findIndex((item) => item.meta.id === action.payload);
                if (index > -1) {
                    state.data.splice(index, 1);
                }
            });
    },
});

export default templatesSlice.reducer;
