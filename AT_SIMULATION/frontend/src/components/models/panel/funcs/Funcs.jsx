import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Link, useMatches, useNavigate, useParams } from "react-router-dom";
import { deleteFunc, loadFuncs } from "../../../../redux/stores/funcsStore";
import { LOAD_STATUSES } from "../../../../GLOBAL";
import { Button, Col, Dropdown, Menu, Modal, Row, Skeleton } from "antd";
import { EditOutlined, PlusOutlined, CopyOutlined, DeleteOutlined, DashOutlined } from "@ant-design/icons";

import "../PanelMenu.css";
import CreateFuncModal from "./dialogs/CreateFuncModal";
import EditFuncModal from "./dialogs/EditFuncModal";

export default ({ closed }) => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const [modal, contextHandler] = Modal.useModal();

    const funcs = useSelector((state) => state.funcs);
    const params = useParams();
    const matches = useMatches();
    const createOpen = Boolean(matches.find((match) => /models\/\d+\/funcs\/new/g.test(match.pathname)));
    const editOpen = Boolean(matches.find((match) => /models\/\d+\/funcs\/\d+\/edit/g.test(match.pathname)));

    useEffect(() => {
        dispatch(loadFuncs(params.modelId));
    }, []);

    const dropDownItems = (func) => [
        {
            key: "edit",
            label: "Редактировать",
            icon: <EditOutlined />,
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

    const handleEditFunc = (func) => navigate(`/models/${params.modelId}/funcs/${func.id}/edit`);

    const handleDuplicateFunc = async (func) => {
        // duplicate func
        // dispatch(duplicateFunc({modelId: params.modelId, funcId: func.id}));
    };

    const handleDeleteFunc = async (func) => {
        // delete func
        await dispatch(deleteFunc({ modelId: params.modelId, funcId: func.id }));
        navigate(`/models/${params.modelId}/funcs`);
    };

    const confirmDeleteFunc = (func) => {
        modal.confirm({
            title: "Удаление функции",
            content: (
                <>
                    Вы уверены, что хотите удалить функцию <b>{func.name}?</b>
                </>
            ),
            okText: "Удалить",
            cancelText: "Отмена",
            icon: <DeleteOutlined />,
            onOk: () => handleDeleteFunc(func),
        });
    };

    const options = {
        edit: handleEditFunc,
        duplicate: handleDuplicateFunc,
        delete: confirmDeleteFunc,
    };

    const className = closed ? ["model-item-menu", "closed"] : ["model-item-menu"];

    return funcs.status === LOAD_STATUSES.SUCCESS ? (
        <div>
            <div className={className.join(' ')}>
                <Menu
                    selectedKeys={[params.funcId]}
                    items={funcs.data.map((func) => {
                        return {
                            key: func.id.toString(),
                            label: (
                                <Row style={{ width: "100%" }} gutter={10}>
                                    <Col flex="auto">
                                        <Link to={`/models/${params.modelId}/funcs/${func.id}`}>{func.name}</Link>
                                    </Col>
                                    <Col>
                                        <Dropdown
                                            trigger={["click"]}
                                            menu={{
                                                items: dropDownItems(func),
                                                onClick: ({ key }) => options[key](func),
                                            }}
                                        >
                                            <Button size="small" icon={<DashOutlined />} />
                                        </Dropdown>
                                    </Col>
                                </Row>
                            ),
                        };
                    })}
                />
            </div>
            <Link to={`/models/${params.modelId}/funcs/new`}>
                <Button type="primary" style={{ width: "100%" }} icon={<PlusOutlined />}>
                    Создать функцию
                </Button>
            </Link>
            {createOpen ? <CreateFuncModal open={createOpen} /> : <></>}
            {editOpen ? <EditFuncModal open={editOpen} /> : <></>}
            {contextHandler}
        </div>
    ) : (
        <Skeleton active />
    );
};
