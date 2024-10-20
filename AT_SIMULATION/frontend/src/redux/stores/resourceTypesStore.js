import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { createFrameActionAsyncThunk } from "../frameActor";
import { API_URL, getHeaders, LOAD_STATUSES, MOCKING } from "../../GLOBAL";

export const loadResourceTypes = createAsyncThunk("resourceTypes/load", async (modelId) => {
    const url = `${API_URL}/api/editor/resources/types/`;
    const headers = getHeaders({ "model-id": modelId });

    if (MOCKING) {
        console.log(url, {
            headers,
        });
        const json = {
            resource_types: [
                {
                    name: "type1",
                    type: "constant",
                    attributes: [
                        {
                            id: 1,
                            name: "attr1",
                            type: "int",
                            default_value: 5,
                        },
                        {
                            id: 2,
                            name: "attr2",
                            type: "float",
                            default_value: 5.0,
                        },
                        {
                            id: 3,
                            name: "attr3",
                            type: "bool",
                            default_value: true,
                        },
                        {
                            id: 4,
                            name: "attr4",
                            type: "enum",
                            enum_values_set: ["hello", "world"],
                            default_value: "hello",
                        },
                    ],
                    id: 1,
                },
                {
                    name: "type2",
                    type: "temporal",
                    attributes: [
                        {
                            id: 5,
                            name: "attr1",
                            type: "int",
                            default_value: 5,
                        },
                        {
                            id: 6,
                            name: "attr2",
                            type: "float",
                            default_value: 5.0,
                        },
                        {
                            id: 7,
                            name: "attr3",
                            type: "bool",
                            default_value: true,
                        },
                        {
                            id: 8,
                            name: "attr4",
                            type: "enum",
                            enum_values_set: ["hello", "world"],
                            default_value: "hello",
                        },
                    ],
                    id: 2,
                },
            ],
            total: 0,
        };
        return { items: json.resource_types, modelId };
    }

    const response = await fetch(url, {
        headers,
    });
    const json = await response.json();

    return { items: json.resource_types, modelId };
});

export const createResourceType = createFrameActionAsyncThunk("resourceTypes/create", async ({ modelId, resourceType }) => {
    const url = `${API_URL}/api/editor/resources/types/`;
    const headers = getHeaders({ "model-id": modelId });

    if (MOCKING) {
        console.log(url, {
            method: "POST",
            headers,
            body: JSON.stringify(resourceType),
        });
        const json = resourceType;

        if (!json.id) {
            json.id = Math.floor(Math.random() * 10000) + 1;
        }
        json.attributes = json.attributes.map((attr) => ({
            ...attr,
            id: attr.id || Math.floor(Math.random() * 10000) + 1,
        }));
        return json;
    }

    const response = await fetch(url, {
        method: "POST",
        headers,
        body: JSON.stringify(resourceType),
    });
    const json = await response.json();
    return json;
});

export const updateResourceType = createFrameActionAsyncThunk("resourceTypes/update", async ({ modelId, resourceType }) => {
    const url = `${API_URL}/api/editor/resources/types/${resourceType.id}/`;
    const headers = getHeaders({ "model-id": modelId });

    if (MOCKING) {
        console.log(url, {
            method: "PUT",
            headers,
            body: JSON.stringify(resourceType),
        });
        const json = resourceType;
        return json;
    }

    const response = await fetch(url, {
        method: "PUT",
        headers,
        body: JSON.stringify(resourceType),
    });
    const json = await response.json();
    return json;
});

export const deleteResourceType = createFrameActionAsyncThunk("resourceTypes/delete", async ({ modelId, resourceTypeId }) => {
    const url = `${API_URL}/api/editor/resources/types/${resourceTypeId}/`;
    const headers = getHeaders({ "model-id": modelId });
    if (MOCKING) {
        console.log(url, {
            method: "DELETE",
            headers,
        });
        const json = { id: resourceTypeId };
        return json.id;
    }

    const response = await fetch(url, {
        method: "DELETE",
        headers,
    });
    const json = await response.json();
    return json.id;
});

const resourceTypesSlice = createSlice({
    name: "resourceTypes",
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
            .addCase(loadResourceTypes.pending, (state) => {
                state.status = LOAD_STATUSES.LOADING;
            })
            .addCase(loadResourceTypes.fulfilled, (state, action) => {
                state.status = LOAD_STATUSES.SUCCESS;
                state.data = action.payload.items;
                state.modelId = action.payload.modelId;
            })
            .addCase(createResourceType.pending, (state) => {
                state.status = LOAD_STATUSES.LOADING;
            })
            .addCase(createResourceType.fulfilled, (state, action) => {
                state.status = LOAD_STATUSES.SUCCESS;
                state.data.push(action.payload);
            })
            .addCase(updateResourceType.pending, (state) => {
                state.status = LOAD_STATUSES.LOADING;
            })
            .addCase(updateResourceType.fulfilled, (state, action) => {
                state.status = LOAD_STATUSES.SUCCESS;
                const index = state.data.findIndex((item) => item.id === action.payload.id);
                if (index > -1) {
                    state.data[index] = action.payload;
                }
            })
            .addCase(deleteResourceType.pending, (state) => {
                state.status = LOAD_STATUSES.LOADING;
            })
            .addCase(deleteResourceType.fulfilled, (state, action) => {
                state.status = LOAD_STATUSES.SUCCESS;
                const index = state.data.findIndex((item) => item.id === action.payload);
                if (index > -1) {
                    state.data.splice(index, 1);
                }
            });
    },
});

export default resourceTypesSlice.reducer;
