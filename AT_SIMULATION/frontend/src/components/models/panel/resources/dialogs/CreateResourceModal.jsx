import { Button, Form, Modal, Space } from "antd";
import ResourceForm from "../forms/ResourceForm";
import { Link, useNavigate, useParams } from "react-router-dom";
import { PlusOutlined } from "@ant-design/icons";
import { useDispatch, useSelector } from "react-redux";
import { createResource, loadResources } from "../../../../../redux/stores/resourcesStore";
import { useEffect } from "react";
import { loadResourceTypes } from "../../../../../redux/stores/resourceTypesStore";
import { LOAD_STATUSES } from "../../../../../GLOBAL";

export default ({ open, ...modalProps }) => {
    const params = useParams();
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const [form] = Form.useForm();
    const resourceTypes = useSelector((store) => store.resourceTypes);
    const resources = useSelector((store) => store.resources);

    useEffect(() => {
        if (resourceTypes.status !== LOAD_STATUSES.SUCCESS || resourceTypes.modelId !== params.modelId) {
            dispatch(loadResourceTypes(params.modelId));
        }
        if (resources.status !== LOAD_STATUSES.SUCCESS || resources.modelId !== params.modelId) {
            dispatch(loadResources(params.modelId));
        }
    }, []);

    form.setFieldValue("model_id", params.modelId);
    form.setFieldValue("to_be_traced", true);

    const handleCreate = async () => {
        try {
            const data = await form.validateFields();
            const action = await dispatch(createResource({ modelId: params.modelId, resource: data }));
            const resource = action.payload;
            navigate(`/models/${params.modelId}/resources/${resource.id}`);
        } catch (e) {
            console.error("Form validation failed:", e);
        }
    };

    return (
        <Modal
            width={1300}
            open={open}
            title="Добавление нового ресурса"
            onCancel={() => navigate(`/models/${params.modelId}/resources`)}
            footer={
                <Space>
                    <Button type="primary" icon={<PlusOutlined />} onClick={handleCreate}>
                        Создать
                    </Button>
                    <Link to={`/models/${params.modelId}/resources`}>
                        <Button>Отмена</Button>
                    </Link>
                </Space>
            }
            {...modalProps}
        >
            <ResourceForm form={form} resourceTypes={resourceTypes.data} modelId={params.modelId} layout="vertical" resources={resources.data} />
        </Modal>
    );
};
