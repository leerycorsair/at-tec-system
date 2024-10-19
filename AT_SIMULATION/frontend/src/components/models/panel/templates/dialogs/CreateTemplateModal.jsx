import { Button, Form, Modal, Space } from "antd";
import TemplateForm from "../forms/TemplateForm";
import { Link, useNavigate, useParams } from "react-router-dom";
import { PlusOutlined } from "@ant-design/icons";
import { useDispatch, useSelector } from "react-redux";
import { createTemplate, loadTemplates } from "../../../../../redux/stores/templatesStore";
import { useEffect } from "react";
import { loadResourceTypes } from "../../../../../redux/stores/resourceTypesStore";
import { loadFuncs } from "../../../../../redux/stores/funcsStore";
import { LOAD_STATUSES } from "../../../../../GLOBAL";

export default ({ open, ...modalProps }) => {
    const params = useParams();
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const [form] = Form.useForm();
    const resourceTypes = useSelector((store) => store.resourceTypes);
    const templates = useSelector((store) => store.templates);
    const funcs = useSelector((store) => store.funcs);

    useEffect(() => {
        if (resourceTypes.status !== LOAD_STATUSES.SUCCESS || resourceTypes.modelId !== params.modelId) {
            dispatch(loadResourceTypes(params.modelId));
        }
        if (templates.status !== LOAD_STATUSES.SUCCESS || templates.modelId !== params.modelId) {
            dispatch(loadTemplates(params.modelId));
        }
        if (funcs.status !== LOAD_STATUSES.SUCCESS || funcs.modelId !== params.modelId) {
            dispatch(loadFuncs(params.modelId));
        }
    }, []);

    form.setFieldValue("model_id", params.modelId);

    return (
        <Modal
            width={1300}
            open={open}
            title="Добавление нового образца операции"
            onCancel={() => navigate(`/models/${params.modelId}/templates`)}
            footer={
                <Space>
                    <Button
                        type="primary"
                        icon={<PlusOutlined />}
                        onClick={async () => {
                            try {
                                const data = await form.validateFields();
                                const action = await dispatch(createTemplate({ modelId: params.modelId, template: data }));
                                const template = action.payload;
                                navigate(`/models/${params.modelId}/templates/${template.meta.id}`);
                            } catch (e) {
                                console.error("Form validation failed:", e);
                            }
                        }}
                    >
                        Создать
                    </Button>
                    <Link to={`/models/${params.modelId}/templates`}>
                        <Button>Отмена</Button>
                    </Link>
                </Space>
            }
            {...modalProps}
        >
            <TemplateForm modelId={params.modelId} form={form} resourceTypes={resourceTypes.data} layout="vertical" templates={templates.data} funcs={funcs.data} />
        </Modal>
    );
};
