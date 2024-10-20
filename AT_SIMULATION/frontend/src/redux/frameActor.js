import { createAsyncThunk } from "@reduxjs/toolkit";

export const createFrameActionAsyncThunk = (type, payloadCreator, options) => {
    const newPayloadCreator = async (...args) => {
        const result = await payloadCreator(...args);
        if (window.sessionStorage.getItem("frameId")) {
            window.parent.postMessage({ type: "action", event: type, data: { args: args[0], result }, frameId: window.sessionStorage.getItem("frameId") }, "*");
        }
        return result;
    };

    return createAsyncThunk(type, newPayloadCreator, options);
};
