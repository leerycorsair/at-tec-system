export const LOAD_STATUSES = {
    LOADING: "loading",
    LOADED: "loaded",
    SUCCESS: "loaded",
    ERROR: "error",
    IDLE: "idle",
};

export const API_PROTOCOL = process.env.REACT_APP_API_PROTOCOL || window.location.protocol.slice(0, -1);
export const API_HOST = process.env.REACT_APP_API_HOST || window.location.hostname;
export const API_PORT = process.env.REACT_APP_API_PORT || window.location.port;

export const API_URL = process.env.REACT_APP_API_URL || `${API_PROTOCOL}://${API_HOST}:${API_PORT}`;
export const MOCKING = ["true", "false"].includes(String(process.env.REACT_APP_MOCKING)) ? JSON.parse(String(process.env.REACT_APP_MOCKING)) : false;

export const getHeaders = (extra = {}) => ({
    "Content-Type": "application/json",
    Accept: "application/json",
    Authorization: `Bearer ${window.sessionStorage.getItem("token")}`,
    ...extra,
});
