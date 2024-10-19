import { Button, Form, Modal, Space } from "antd";
import TemplateUsageForm from "../forms/TemplateUsageForm";
import { Link, useNavigate, useParams } from "react-router-dom";
import { SaveOutlined } from "@ant-design/icons";
import { useDispatch, useSelector } from "react-redux";
import { updateTemplateUsage } from "../../../../../redux/stores/templateUsagesStore";
import { loadTemplates } from "../../../../../redux/stores/templatesStore";
import { useEffect } from "react";
import { loadResources } from "../../../../../redux/stores/resourcesStore";
import { LOAD_STATUSES } from "../../../../../GLOBAL";

export default ({ open, ...modalProps }) => {
    const params = useParams();
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const [form] = Form.useForm();

    const templateUsages = useSelector((store) => store.templateUsages);
    const templateUsage = templateUsages.data.find((templateUsage) => templateUsage.id.toString() === params.templateUsageId);
    console.log(templateUsage);
    form.setFieldsValue(templateUsage);

    const templates = useSelector((store) => store.templates);
    const resources = useSelector((store) => store.resources);
    useEffect(() => {
        if (resources.status !== LOAD_STATUSES.SUCCESS || resources.modelId !== params.modelId) {
            dispatch(loadResources(params.modelId));
        }
        if (templates.status !== LOAD_STATUSES.SUCCESS || templates.modelId !== params.modelId) {
            dispatch(loadTemplates(params.modelId));
        }
    }, []);

    const handleEdit = async () => {
        try {
            const data = await form.validateFields();
            console.log(data);
            const action = await dispatch(updateTemplateUsage({ modelId: params.modelId, templateUsage: data }));
            const updatedTemplateUsage = action.payload;
            navigate(`/models/${params.modelId}/templateUsages/${updatedTemplateUsage.id}`);
        } catch (err) {
            console.error("Form validation failed:", err);
        }
    };

    return (
        <Modal
            width={1300}
            open={open}
            title="Редактирование операции"
            onCancel={() => navigate(`/models/${params.modelId}/template-usages/${params.templateUsageId}`)}
            footer={
                <Space>
                    <Button type="primary" icon={<SaveOutlined />} onClick={handleEdit}>
                        Сохранить
                    </Button>
                    <Link to={`/models/${params.modelId}/template-usages/${params.templateUsageId}`}>
                        <Button>Отмена</Button>
                    </Link>
                </Space>
            }
            {...modalProps}
        >
            <TemplateUsageForm resources={resources.data} templates={templates.data} form={form} modelId={params.modelId} layout="vertical" templateUsages={templateUsages.data} />
        </Modal>
    );
};
