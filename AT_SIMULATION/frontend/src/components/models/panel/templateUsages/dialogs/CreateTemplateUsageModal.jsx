import { Button, Form, Modal, Space } from "antd";
import TemplateUsageForm from "../forms/TemplateUsageForm";
import { Link, useNavigate, useParams } from "react-router-dom";
import { PlusOutlined } from "@ant-design/icons";
import { useDispatch, useSelector } from "react-redux";
import { createTemplateUsage } from "../../../../../redux/stores/templateUsagesStore";
import { useEffect } from "react";
import { loadResources } from "../../../../../redux/stores/resourcesStore";
import { loadTemplates } from "../../../../../redux/stores/templatesStore";
import { LOAD_STATUSES } from "../../../../../GLOBAL";

export default ({ open, ...modalProps }) => {
    const params = useParams();
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const [form] = Form.useForm();
    const resources = useSelector((store) => store.resources);
    const templates = useSelector((store) => store.templates);
    const templateUsages = useSelector((store) => store.templateUsages);

    useEffect(() => {
        if (resources.status !== LOAD_STATUSES.SUCCESS || resources.modelId !== params.modelId) {
            dispatch(loadResources(params.modelId));
        }
        if (templates.status !== LOAD_STATUSES.SUCCESS || templates.modelId !== params.modelId) {
            dispatch(loadTemplates(params.modelId));
        }
    }, []);

    form.setFieldValue("model_id", params.modelId);

    return (
        <Modal
            width={1300}
            open={open}
            title="Добавление новой операции"
            onCancel={() => navigate(`/models/${params.modelId}/template-usages`)}
            footer={
                <Space>
                    <Button
                        type="primary"
                        icon={<PlusOutlined />}
                        onClick={async () => {
                            try {
                                const data = await form.validateFields();
                                const action = await dispatch(createTemplateUsage({ modelId: params.modelId, templateUsage: data }));
                                const templateUsage = action.payload;
                                navigate(`/models/${params.modelId}/template-usages/${templateUsage.id}`);
                            } catch (e) {
                                console.error("Form validation failed:", e);
                            }
                        }}
                    >
                        Создать
                    </Button>
                    <Link to={`/models/${params.modelId}/template-usages`}>
                        <Button>Отмена</Button>
                    </Link>
                </Space>
            }
            {...modalProps}
        >
            <TemplateUsageForm modelId={params.modelId} form={form} resources={resources.data} templates={templates.data} layout="vertical" templateUsages={templateUsages.data} />
        </Modal>
    );
};
