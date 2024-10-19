import { Button, Form, Modal, Space } from "antd";
import TemplateForm from "../forms/TemplateForm";
import { Link, useNavigate, useParams } from "react-router-dom";
import { SaveOutlined } from "@ant-design/icons";
import { useDispatch, useSelector } from "react-redux";
import { loadTemplates, updateTemplate } from "../../../../../redux/stores/templatesStore";
import { useEffect } from "react";
import { loadResourceTypes } from "../../../../../redux/stores/resourceTypesStore";
import { loadFuncs } from "../../../../../redux/stores/funcsStore";
import { LOAD_STATUSES } from "../../../../../GLOBAL";

export default ({ open, ...modalProps }) => {
    const params = useParams();
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const [form] = Form.useForm();

    debugger;

    const templates = useSelector((store) => store.templates);
    const template = templates.data.find((template) => template.meta.id.toString() === params.templateId);
    form.setFieldsValue(template);

    const resourceTypes = useSelector((store) => store.resourceTypes);
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

    return (
        <Modal
            width={1300}
            open={open}
            title="Редактирование образца операции"
            onCancel={() => navigate(`/models/${params.modelId}/templates/${params.templateId}`)}
            footer={
                <Space>
                    <Button
                        type="primary"
                        icon={<SaveOutlined />}
                        onClick={async () => {
                            try {
                                const data = await form.validateFields();
                                const action = await dispatch(updateTemplate({ modelId: params.modelId, template: data }));
                                const updatedTemplate = action.payload;
                                navigate(`/models/${params.modelId}/templates/${updatedTemplate.meta.id}`);
                            } catch (err) {
                                console.error("Form validation failed:", err);
                            }
                        }}
                    >
                        Сохранить
                    </Button>
                    <Link to={`/models/${params.modelId}/templates/${params.templateId}`}>
                        <Button>Отмена</Button>
                    </Link>
                </Space>
            }
            {...modalProps}
        >
            <TemplateForm modelId={params.modelId} resourceTypes={resourceTypes.data} form={form} layout="vertical" templates={templates.data} funcs={funcs.data} />
        </Modal>
    );
};
