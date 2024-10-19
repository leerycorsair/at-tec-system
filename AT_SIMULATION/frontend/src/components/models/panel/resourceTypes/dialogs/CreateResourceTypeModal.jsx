import { Button, Form, Modal, Space } from "antd";
import ResourceTypeForm from "../forms/ResourceTypeForm";
import { Link, useNavigate, useParams } from "react-router-dom";
import { PlusOutlined } from "@ant-design/icons";
import { useDispatch, useSelector } from "react-redux";
import { createResourceType, loadResourceTypes } from "../../../../../redux/stores/resourceTypesStore";
import { useEffect } from "react";
import { LOAD_STATUSES } from "../../../../../GLOBAL";

export default ({ open, ...modalProps }) => {
    const params = useParams();
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const [form] = Form.useForm();

    form.setFieldValue("model_id", params.modelId);
    const resourceTypes = useSelector((store) => store.resourceTypes);

    useEffect(() => {
        if (resourceTypes.status !== LOAD_STATUSES.SUCCESS || resourceTypes.modelId !== params.modelId) {
            dispatch(loadResourceTypes(params.modelId));
        }
    }, [])

    return (
        <Modal
            width={1300}
            open={open}
            title="Добавление нового типа ресурса"
            onCancel={() => navigate(`/models/${params.modelId}/resource-types`)}
            footer={
                <Space>
                    <Button
                        type="primary"
                        icon={<PlusOutlined />}
                        onClick={async () => {
                            try {
                                const data = await form.validateFields();
                                const action = await dispatch(createResourceType({ modelId: params.modelId, resourceType: data }));
                                const resourceType = action.payload;
                                navigate(`/models/${params.modelId}/resource-types/${resourceType.id}`);
                            } catch (e) {
                                console.error("Form validation failed:", e);
                            }
                        }}
                    >
                        Создать
                    </Button>
                    <Link to={`/models/${params.modelId}/resource-types`}>
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
