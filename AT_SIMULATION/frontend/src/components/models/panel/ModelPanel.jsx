import { Empty, Tabs } from "antd";
import { useMatches, useNavigate, useParams } from "react-router-dom";
import "./ModelPanel.css";
import ResourceTypes from "./resourceTypes/ResourceTypes";
import Resources from "./resources/Resources";
import Templates from "./templates/Templates";
import TemplateUsages from "./templateUsages/TemplateUsages";
import Funcs from "./funcs/Funcs";

export default ({ panelOpen }) => {
    const navigate = useNavigate();
    const params = useParams();
    const matches = useMatches();
    const keyPath = matches[2]?.pathname?.split("/")[3];
    const defaultActiveKey = ["resource-types", "resources", "templates", "template-usages", "funcs"].includes(keyPath) ? keyPath : null;

    const tabStyle = panelOpen ? {} : { writingMode: "vertical-lr" };
    const tabPosition = panelOpen ? "top" : "left";

    const panelClassNames = panelOpen ? ["model-panel"] : ["model-panel", "closed"];

    return (
        <div style={{ background: "white", padding: 10, paddingTop: 0, paddingLeft: 0 }}>
            <Tabs
                tabPosition={tabPosition}
                className={panelClassNames}
                activeKey={defaultActiveKey}
                size="small"
                tabBarStyle={panelOpen ? { marginLeft: 15 } : { width: 50 }}
                onTabClick={(activeKey) => navigate(`/models/${params.modelId}/${activeKey}`)}
                items={[
                    {
                        key: "resource-types",
                        label: <div style={tabStyle}>Типы ресурсов</div>,
                        children: <ResourceTypes closed={!panelOpen} />,
                    },
                    {
                        key: "resources",
                        label: <div style={tabStyle}>Ресурсы</div>,
                        children: <Resources closed={!panelOpen} />,
                    },
                    {
                        key: "templates",
                        label: <div style={tabStyle}>Образцы операций</div>,
                        children: <Templates closed={!panelOpen} />,
                    },
                    {
                        key: "template-usages",
                        label: <div style={tabStyle}>Операции</div>,
                        children: <TemplateUsages closed={!panelOpen} />,
                    },
                    {
                        key: "funcs",
                        label: <div style={tabStyle}>Функции</div>,
                        children: <Funcs closed={!panelOpen} />,
                    },
                ]}
            />
            {!defaultActiveKey && panelOpen ? <Empty description="Выберите сущность ИМ" /> : <></>}
        </div>
    );
};
