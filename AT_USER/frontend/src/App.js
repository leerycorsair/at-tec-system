import React from "react";

import { Button, Form, Grid, Input, theme, Typography, message } from "antd";

import { LockOutlined, LoginOutlined, UserOutlined } from "@ant-design/icons";

const { useToken } = theme;
const { useBreakpoint } = Grid;
const { Title } = Typography;

const loadHref = (href, target = "_self") => {
    const a = window.document.createElement("a");
    a.href = href;
    a.target = target;
    a.click();
};

const doLogin = async (data) => {
    const API_PROTOCOL = process.env.REACT_APP_API_PROTOCOL || window.location.protocol.slice(0, -1);
    const API_HOST = process.env.REACT_APP_API_HOST || window.location.hostname;
    const API_PORT = process.env.REACT_APP_API_PORT || window.location.port;

    const apiUrl = `${API_PROTOCOL}://${API_HOST}:${API_PORT}`;
    const url = `${apiUrl}/api/auth/sign_in`;
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    if (response.ok) {
        const json = await response.json();
        return json;
    }

    const text = await response.text();

    throw new Error("Failed to login", { cause: { status: response.status, text } });
};

export default () => {
    const { token } = useToken();
    const screens = useBreakpoint();

    const onFinish = async (values) => {
        try {
            const { token } = await doLogin(values);
            const search = new window.URLSearchParams(window.location.search);

            if (search.has("to")) {
                const to = new URL(search.get("to"));
                const tokenField = search.get("token_field") || "token";

                const redirectSearch = new window.URLSearchParams(to.search);
                redirectSearch.set(tokenField, token);
                to.search = redirectSearch.toString();

                loadHref(to.toString());
            } else {
                message.success("Вход выполнен успешно");
            }
        } catch (error) {
            console.error("Failed to login", error);
            if (error.cause?.status === 401 || error.cause?.status === 403) {
                message.error("Неверные логин или пароль");
            } else {
                message.error("Ошибка входа");
            }
        }
    };

    const styles = {
        container: {
            margin: "0 auto",
            padding: screens.md ? `${token.paddingXL}px` : `${token.sizeXXL}px ${token.padding}px`,
            width: "380px",
        },
        footer: {
            marginTop: token.marginLG,
            textAlign: "center",
            width: "100%",
        },
        forgotPassword: {},
        register: {
            float: "right",
        },
        header: {
            marginBottom: token.marginXL,
            textAlign: "center",
        },
        section: {
            alignItems: "center",
            backgroundColor: token.colorBgContainer,
            display: "flex",
            padding: screens.md ? `${token.sizeXXL}px 0px` : "0px",
        },
        text: {
            color: token.colorTextSecondary,
        },
        title: {
            fontSize: screens.md ? token.fontSizeHeading2 : token.fontSizeHeading3,
        },
    };

    return (
        <section style={styles.section}>
            <div style={styles.container}>
                <div style={styles.header}>
                    <Title style={styles.title}>Вход в систему</Title>
                </div>
                <Form onFinish={onFinish} layout="vertical" requiredMark="optional">
                    <Form.Item
                        name="login"
                        rules={[
                            {
                                required: true,
                                message: "Укажите логин",
                            },
                        ]}
                    >
                        <Input prefix={<UserOutlined />} placeholder="Логин" />
                    </Form.Item>
                    <Form.Item
                        name="password"
                        rules={[
                            {
                                required: true,
                                message: "Укажите пароль!",
                            },
                        ]}
                    >
                        <Input.Password prefix={<LockOutlined />} type="password" placeholder="Пароль" />
                    </Form.Item>
                    <Form.Item>
                        <Button block="true" icon={<LoginOutlined />} type="primary" htmlType="submit">
                            Войти
                        </Button>
                    </Form.Item>
                    <a style={styles.forgotPassword} href="">
                        Забыли пароль?
                    </a>
                    <a style={styles.register} href="">
                        Зарегистрироваться
                    </a>
                </Form>
            </div>
        </section>
    );
};
