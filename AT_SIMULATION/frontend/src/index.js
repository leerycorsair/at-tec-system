import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import { Provider } from "react-redux";
import store from "./redux/store";
import { ConfigProvider } from "antd";

window.onload = function () {
    window.addEventListener("beforeunload", function (e) {
        var confirmationMessage = "Убедитесь, что все изменения сохранены.";

        (e || window.event).returnValue = confirmationMessage; //Gecko + IE
        return confirmationMessage; //Gecko + Webkit, Safari, Chrome etc.
    });
};

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
    <Provider store={store}>
        <ConfigProvider
            theme={{
                cssVar: true,
                token: { borderRadius: 2, colorBorder: "#cccccc", colorBorderSecondary: "#e0e0e0" },
            }}
        >
            <App />
        </ConfigProvider>
    </Provider>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
