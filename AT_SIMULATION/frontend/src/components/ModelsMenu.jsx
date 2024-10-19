import { useSelector, useDispatch } from "react-redux";
import { Button, Col, Dropdown, Menu, Row, Skeleton, Modal, Form, theme } from "antd";
import { useParams, useNavigate, useMatches } from "react-router-dom";
import { LOAD_STATUSES } from "../GLOBAL";
import { useEffect } from "react";
import { createModel, deleteModel, loadModels } from "../redux/stores/modelsStore";

import "./ModelsMenu.css";
import { CopyOutlined, DashOutlined, DeleteOutlined, PlusCircleFilled, PlusOutlined, SaveOutlined, UploadOutlined } from "@ant-design/icons";
import CreateModelForm from "./models/forms/CreateModelForm";

export default () => {
    const dispatch = useDispatch();
    const [modal, contextHandler] = Modal.useModal();
    const models = useSelector((state) => state.models);
    const params = useParams();
    const currentModelId = params.modelId;
    const navigate = useNavigate();
    const [createForm] = Form.useForm();
    const matches = useMatches();
    const createOpen = Boolean(matches.find((match) => /models\/new/g.test(match.pathname)));

    const {
        token: { colorInfoText },
    } = theme.useToken();

    const dropDownItems = [
        {
            key: "export",
            label: "Экспортировать",
            icon: <SaveOutlined />,
        },
        {
            key: "duplicate",
            label: "Дублировать",
            icon: <CopyOutlined />,
        },
        {
            key: "delete",
            label: "Удалить",
            icon: <DeleteOutlined />,
            danger: true,
        },
    ];

    const handleExport = (model) => {};

    const handleDelete = async (model) => {
        await dispatch(deleteModel(model.id));
        if (params.modelId === model.id.toString()) {
            navigate("/");
        }
    };

    const confirmDelete = (model) =>
        modal.confirm({
            title: "Удаление имитационной модели",
            content: (
                <>
                    Удалить имитационную модель <b>{model.name}?</b>
                </>
            ),
            okText: "Удалить",
            cancelText: "Отмена",
            icon: <DeleteOutlined />,
            onOk: () => handleDelete(model),
        });

    const dropdownHandlers = {
        export: (model) => console.log(model),
        duplicate: (model) => console.log(model),
        delete: confirmDelete,
    };

    const handleCreate = async (form) => {
        const data = await form.validateFields();
        const result = await dispatch(createModel(data));
        navigate(`/models/${result.payload.id}`);
    };

    const confirmCreateModel = async () => {
        try {
            await modal.confirm({
                title: "Создание имитационной модели",
                content: <CreateModelForm form={createForm} layout="vertical" models={models.data} />,
                onOk: () => handleCreate(createForm),
                okText: "Создать",
                cancelText: "Отмена",
                closable: true,
                icon: <PlusCircleFilled style={{ color: colorInfoText }} />,
            });
        } catch (e) {}
    };

    const items = models?.data?.map((model) => ({
        key: model.id.toString(),
        label: (
            <Row style={{ width: "100%" }} gutter={10}>
                <Col flex="auto">{model.name}</Col>
                <Col>
                    <Dropdown
                        trigger={["click"]}
                        menu={{
                            items: dropDownItems,
                            onClick: ({ key, domEvent }) => {
                                domEvent.stopPropagation();
                                dropdownHandlers[key](model);
                            },
                        }}
                    >
                        <Button size="small" icon={<DashOutlined />} onClick={(e) => e.stopPropagation()} />
                    </Dropdown>
                </Col>
            </Row>
        ),
    }));

    useEffect(() => {
        dispatch(loadModels());
    }, []);

    useEffect(() => {
        if (createOpen) {
            setTimeout(confirmCreateModel, 500);
        }
    }, [createOpen]);

    return models.status === LOAD_STATUSES.SUCCESS ? (
        <div className="sider-model-menu-wrapper">
            <div>
                <Menu onSelect={({ key }) => navigate(`/models/${key}`)} className="sider-model-menu" selectedKeys={[currentModelId]} items={items} />
            </div>
            <div style={{ marginBottom: 10 }}>
                <Button icon={<PlusOutlined />} onClick={confirmCreateModel} style={{ width: "100%" }}>
                    Создать модель
                </Button>
            </div>
            <div>
                <Button icon={<UploadOutlined />} style={{ width: "100%" }}>
                    Загрузить модель
                </Button>
            </div>
            {contextHandler}
        </div>
    ) : (
        <div className="sider-model-menu-wrapper" style={{ background: "white" }}>
            <Skeleton active />
        </div>
    );
};
