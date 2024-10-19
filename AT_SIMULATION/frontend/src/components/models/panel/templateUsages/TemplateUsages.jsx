import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Link, useMatches, useNavigate, useParams } from "react-router-dom";
import { deleteTemplateUsage, loadTemplateUsages } from "../../../../redux/stores/templateUsagesStore";
import { LOAD_STATUSES } from "../../../../GLOBAL";
import { Button, Col, Dropdown, Menu, Modal, Row, Skeleton } from "antd";
import { EditOutlined, PlusOutlined, CopyOutlined, DeleteOutlined, DashOutlined } from "@ant-design/icons";

import "../PanelMenu.css";
import CreateTemplateUsageModal from "./dialogs/CreateTemplateUsageModal";
import EditTemplateUsageModal from "./dialogs/EditTemplateUsageModal";

export default ({closed}) => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const [modal, contextHandler] = Modal.useModal();

    const templateUsages = useSelector((state) => state.templateUsages);
    const params = useParams();
    const matches = useMatches();
    const createOpen = Boolean(matches.find((match) => /models\/\d+\/template-usages\/new/g.test(match.pathname)));
    const editOpen = Boolean(matches.find((match) => /models\/\d+\/template-usages\/\d+\/edit/g.test(match.pathname)));

    useEffect(() => {
        dispatch(loadTemplateUsages(params.modelId));
    }, []);

    const dropDownItems = () => [
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

    const handleEditTemplateUsage = (templateUsage) => navigate(`/models/${params.modelId}/template-usages/${templateUsage.id}/edit`);

    const handleDuplicateTemplateUsage = async (templateUsage) => {
        // duplicate templateUsage
        // dispatch(duplicateTemplateUsage({modelId: params.modelId, templateUsageId: templateUsage.id}));
    };

    const handleDeleteTemplateUsage = async (templateUsage) => {
        // delete templateUsage
        await dispatch(deleteTemplateUsage({ modelId: params.modelId, templateUsageId: templateUsage.id }));
        navigate(`/models/${params.modelId}/template-usages`);
    };

    const confirmDeleteTemplateUsage = (templateUsage) => {
        modal.confirm({
            title: "Удаление операции",
            content: (
                <>
                    Вы уверены, что хотите удалить операцию <b>{templateUsage.name}?</b>
                </>
            ),
            okText: "Удалить",
            cancelText: "Отмена",
            icon: <DeleteOutlined />,
            onOk: () => handleDeleteTemplateUsage(templateUsage),
        });
    };

    const options = {
        edit: handleEditTemplateUsage,
        duplicate: handleDuplicateTemplateUsage,
        delete: confirmDeleteTemplateUsage,
    };

    const className = closed ? ["model-item-menu", "closed"] : ["model-item-menu"];

    return templateUsages.status === LOAD_STATUSES.SUCCESS ? (
        <div>
            <div className={className.join(' ')}>
                <Menu
                    selectedKeys={[params.templateUsageId]}
                    items={templateUsages.data.map((templateUsage) => {
                        return {
                            key: templateUsage.id.toString(),
                            label: (
                                <Row wrap={false} style={{ width: "100%" }} gutter={10}>
                                    <Col flex="auto">
                                        <Link to={`/models/${params.modelId}/template-usages/${templateUsage.id}`}>{templateUsage.name}</Link>
                                    </Col>
                                    <Col>
                                        <Dropdown
                                            trigger={["click"]}
                                            menu={{
                                                items: dropDownItems(templateUsage),
                                                onClick: ({ key }) => options[key](templateUsage),
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
            <Link to={`/models/${params.modelId}/template-usages/new`}>
                <Button type="primary" style={{ width: "100%" }} icon={<PlusOutlined />}>
                    Создать операцию
                </Button>
            </Link>
            {createOpen ? <CreateTemplateUsageModal open={createOpen} /> : <></>}
            {editOpen ? <EditTemplateUsageModal open={editOpen} /> : <></>}
            {contextHandler}
        </div>
    ) : (
        <Skeleton active />
    );
};
