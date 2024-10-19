import { LeftOutlined, RightOutlined } from "@ant-design/icons";
import { Row, Col, Button, Typography } from "antd";
import { useState } from "react";
import { Outlet } from "react-router-dom";
import ModelPanel from "./panel/ModelPanel";

export default () => {
    const [panelOpen, setPanelOpen] = useState(true);
    return (
        <Row>
            <Col style={panelOpen ? { width: 0, transition: "0.5s" } : { transition: "0.5s" }} flex={panelOpen ? null : "auto"}>
                <div
                    style={{
                        height: "100%",
                        visibility: panelOpen ? "hidden" : "visible",
                        transition: "0.5s",
                    }}
                >
                    <Outlet />
                </div>
            </Col>
            <Col style={{ transition: "0.5s", marginLeft: panelOpen ? 0 : 10 }} flex={panelOpen ? "auto" : "none"}>
                <Row style={{ background: "white", padding: 10 }}>
                    <Col>
                        <Button onClick={() => setPanelOpen(!panelOpen)} icon={panelOpen ? <RightOutlined /> : <LeftOutlined />} />
                    </Col>
                    <Col flex="auto">
                        <Typography.Title style={{ margin: 5 }} level={5}>
                            Панель выбора и редактирования сущностей ИМ
                        </Typography.Title>
                    </Col>
                </Row>
                <ModelPanel panelOpen={panelOpen}/>
            </Col>
        </Row>
    );
};
