import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Link, useMatches, useNavigate, useParams } from "react-router-dom";
import { deleteResourceType, loadResourceTypes } from "../../../../redux/stores/resourceTypesStore";
import { LOAD_STATUSES } from "../../../../GLOBAL";
import { Button, Col, Dropdown, Menu, Modal, Row, Skeleton } from "antd";
import { EditOutlined, PlusOutlined, CopyOutlined, DeleteOutlined, DashOutlined } from "@ant-design/icons";

import "../PanelMenu.css";
import CreateResourceTypeModal from "./dialogs/CreateResourceTypeModal";
import EditResourceTypeModal from "./dialogs/EditResourceTypeModal";

export default ({ closed }) => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const [modal, contextHandler] = Modal.useModal();

    const resourceTypes = useSelector((state) => state.resourceTypes);
    const params = useParams();
    const matches = useMatches();
    const createOpen = Boolean(matches.find((match) => /models\/\d+\/resource-types\/new/g.test(match.pathname)));
    const editOpen = Boolean(matches.find((match) => /models\/\d+\/resource-types\/\d+\/edit/g.test(match.pathname)));

    useEffect(() => {
        dispatch(loadResourceTypes(params.modelId));
    }, []);

    const dropDownItems = (resourceType) => [
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

    const handleEditResourceType = (resourceType) => navigate(`/models/${params.modelId}/resource-types/${resourceType.id}/edit`);

    const handleDuplicateResourceType = async (resourceType) => {
        // duplicate resourceType
        // dispatch(duplicateResourceType({modelId: params.modelId, resourceTypeId: resourceType.id}));
    };

    const handleDeleteResourceType = async (resourceType) => {
        // delete resourceType
        await dispatch(deleteResourceType({ modelId: params.modelId, resourceTypeId: resourceType.id }));
        navigate(`/models/${params.modelId}/resource-types`);
    };

    const confirmDeleteResourceType = (resourceType) => {
        modal.confirm({
            title: "Удаление типа ресурса",
            content: (
                <>
                    Вы уверены, что хотите удалить тип рисурса <b>{resourceType.name}?</b>
                </>
            ),
            okText: "Удалить",
            cancelText: "Отмена",
            icon: <DeleteOutlined />,
            onOk: () => handleDeleteResourceType(resourceType),
        });
    };

    const options = {
        edit: handleEditResourceType,
        duplicate: handleDuplicateResourceType,
        delete: confirmDeleteResourceType,
    };

    const className = closed ? ["model-item-menu", "closed"] : ["model-item-menu"];

    return resourceTypes.status === LOAD_STATUSES.SUCCESS ? (
        <div>
            <div className={className.join(' ')}>
                <Menu
                    selectedKeys={[params.resourceTypeId]}
                    items={resourceTypes.data.map((resourceType) => {
                        return {
                            key: resourceType.id.toString(),
                            label: (
                                <Row style={{ width: "100%" }} gutter={10}>
                                    <Col flex="auto">
                                        <Link to={`/models/${params.modelId}/resource-types/${resourceType.id}`}>{resourceType.name}</Link>
                                    </Col>
                                    <Col>
                                        <Dropdown
                                            trigger={["click"]}
                                            menu={{
                                                items: dropDownItems(resourceType),
                                                onClick: ({ key }) => options[key](resourceType),
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
            <Link to={`/models/${params.modelId}/resource-types/new`}>
                <Button type="primary" style={{ width: "100%" }} icon={<PlusOutlined />}>
                    Создать тип ресурса
                </Button>
            </Link>
            {createOpen ? <CreateResourceTypeModal open={createOpen} /> : <></>}
            {editOpen ? <EditResourceTypeModal open={editOpen} /> : <></>}
            {contextHandler}
        </div>
    ) : (
        <Skeleton active />
    );
};
