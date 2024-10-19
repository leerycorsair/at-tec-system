import {Form, Input} from "antd"
import { itemUniqueBetweenRule, requiredRule } from "../../../utils/validators/general"

export default ({ form, models, ...props }) => {

    const [actualForm] = form ? [form] : Form.useForm()

    const getItems = () => (models || []).filter(item => item.id !== actualForm.getFieldValue("id"))
    const getValue = () => actualForm.getFieldsValue()
    const compare = (v, i) => v.name === i.name;

    const uniqueRule = itemUniqueBetweenRule(getValue, getItems, compare)
    
    return <Form form={actualForm} {...props}>
        <Form.Item name="name" rules={[requiredRule, uniqueRule]} label="Название модели">
            <Input placeholder="Укажите название" />
        </Form.Item>
    </Form>
}