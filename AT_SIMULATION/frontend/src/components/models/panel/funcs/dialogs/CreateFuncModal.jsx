import { Button, Form, Modal, Space } from "antd";
import FuncForm from "../forms/FuncForm";
import { Link, useNavigate, useParams } from "react-router-dom";
import { PlusOutlined } from "@ant-design/icons";
import { useDispatch, useSelector } from "react-redux";
import { createFunc, loadFuncs } from "../../../../../redux/stores/funcsStore";
import { useEffect } from "react";
import { LOAD_STATUSES } from "../../../../../GLOBAL";

export default ({ open, ...modalProps }) => {
    const params = useParams();
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const [form] = Form.useForm();

    const funcs = useSelector((store) => store.funcs);

    useEffect(() => {
        if (funcs.status !== LOAD_STATUSES.SUCCESS || funcs.modelId !== params.modelId) {
            dispatch(loadFuncs(params.modelId));
        }
    }, []);

    form.setFieldValue("model_id", params.modelId);

    return (
        <Modal
            width={1300}
            open={open}
            title="Добавление новой функции"
            onCancel={() => navigate(`/models/${params.modelId}/funcs`)}
            footer={
                <Space>
                    <Button
                        type="primary"
                        icon={<PlusOutlined />}
                        onClick={async () => {
                            try {
                                const data = await form.validateFields();
                                const action = await dispatch(createFunc({ modelId: params.modelId, func: data }));
                                const func = action.payload;
                                navigate(`/models/${params.modelId}/funcs/${func.id}`);
                            } catch (e) {
                                console.error("Form validation failed:", e);
                            }
                        }}
                    >
                        Создать
                    </Button>
                    <Link to={`/models/${params.modelId}/funcs`}>
                        <Button>Отмена</Button>
                    </Link>
                </Space>
            }
            {...modalProps}
        >
            <FuncForm form={form} layout="vertical" funcs={funcs.data}/>
        </Modal>
    );
};
