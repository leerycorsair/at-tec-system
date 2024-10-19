import { Form, Input, Select } from "antd";
import { requiredRule, itemUniqueBetweenRule } from "../../../../../utils/validators/general";
import { goIdentifierRule } from "../../../../../utils/validators/go";
import AttributesFormList from "./attributes/AttributesList";

export default ({ form, resourceTypes, ...formProps }) => {
    const [actualForm] = form ? [form] : Form.useForm();
    const typeOptions = [
        {
            label: "Постоянный",
            value: "constant",
        },
        {
            label: "Временный",
            value: "temporal",
        },
    ];

    const getItems = () => (resourceTypes || []).filter(item => item.id !== actualForm.getFieldValue("id"))
    const getValue = () => actualForm.getFieldsValue()
    const compare = (v, i) => v.name === i.name;

    const uniqueRule = itemUniqueBetweenRule(getValue, getItems, compare)

    return (
        <Form form={actualForm} {...formProps}>
            <Form.Item name="id" hidden />
            <Form.Item name="model_id" hidden />
            <Form.Item name="name" label="Имя типа ресурса" rules={[requiredRule, goIdentifierRule, uniqueRule]}>
                <Input placeholder="Укажите имя типа ресурса" />
            </Form.Item>
            <Form.Item name="type" label="Тип" rules={[requiredRule]}>
                <Select placeholder="Выберите тип" options={typeOptions} />
            </Form.Item>
            <Form.Item label="Параметры">
                <Form.List name="attributes">{(fields, { add, remove }) => <AttributesFormList fields={fields} add={add} remove={remove} form={actualForm} />}</Form.List>
            </Form.Item>
        </Form>
    );
};
