import { Button, Form, Modal, Space } from "antd";
import ResourceTypeForm from "../forms/ResourceTypeForm";
import { Link, useNavigate, useParams } from "react-router-dom";
import { SaveOutlined } from "@ant-design/icons";
import { useDispatch, useSelector } from "react-redux";
import { loadResourceTypes, updateResourceType } from "../../../../../redux/stores/resourceTypesStore";
import { useEffect } from "react";
import { LOAD_STATUSES } from "../../../../../GLOBAL";

export default ({ open, ...modalProps }) => {
    const params = useParams();
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const [form] = Form.useForm();

    const resourceTypes = useSelector((store) => store.resourceTypes);
    const resourceType = resourceTypes.data.find(
        (resourceType) => resourceType.id.toString() === params.resourceTypeId
    );
    form.setFieldsValue(resourceType);

    useEffect(() => {
        if (resourceTypes.status !== LOAD_STATUSES.SUCCESS || resourceTypes.modelId !== params.modelId) {
            dispatch(loadResourceTypes(params.modelId));
        }
    }, [])

    return (
        <Modal
            width={1300}
            open={open}
            title="Редактирование типа ресурса"
            onCancel={() => navigate(`/models/${params.modelId}/resource-types/${params.resourceTypeId}`)}
            footer={
                <Space>
                    <Button
                        type="primary"
                        icon={<SaveOutlined />}
                        onClick={async () => {
                            try {
                                const data = await form.validateFields();
                                const action = await dispatch(
                                    updateResourceType({ modelId: params.modelId, resourceType: data })
                                );
                                const updatedResourceType = action.payload;
                                navigate(`/models/${params.modelId}/resource-types/${updatedResourceType.id}`);
                            } catch (err) {
                                console.error("Form validation failed:", err);
                            }
                        }}
                    >
                        Сохранить
                    </Button>
                    <Link to={`/models/${params.modelId}/resource-types/${params.resourceTypeId}`}>
                        <Button>Отмена</Button>
                    </Link>
                </Space>
            }
            {...modalProps}
        >
            <ResourceTypeForm form={form} layout="vertical" resourceTypes={resourceTypes.data}/>
        </Modal>
    );
};
