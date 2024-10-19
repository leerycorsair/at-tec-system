import { Result, Spin } from "antd";
import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";

export default () => {
    const [search, _] = useSearchParams();
    const navigate = useNavigate();
    const token = search.get("token");
    const to = search.get("to") || "/";
    const remember = search.get("remember");
    const frameId = search.get("frame_id");
    const parentOrigin = search.get("parent_origin");

    useEffect(() => {
        if (remember) {
            window.localStorage.setItem("token", token);
        }
        window.sessionStorage.setItem("token", token);

        if (frameId) {
            window.sessionStorage.setItem("frameId", frameId);
        }
        if (parentOrigin) {
            window.sessionStorage.setItem("parentOrigin", parentOrigin);
        }
        navigate(window.decodeURIComponent(to));
    }, []);

    return <Result icon={<Spin />} title="Аутентификация..." />;
};
