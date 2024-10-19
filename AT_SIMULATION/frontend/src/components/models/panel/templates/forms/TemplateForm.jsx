import { Button, Col, Form, Input, InputNumber, Row, Select, Space, Typography, theme } from "antd";
import TinyFormItem from "../../../../../utils/TinyFormItem";
import { CloseOutlined, EyeOutlined, PlusOutlined } from "@ant-design/icons";
import IrregularEventBody from "./body/IrregularEventBody";
import { useState } from "react";
import OperationBody from "./body/OperationBody";
import RuleBody from "./body/RuleBody";
import { Link } from "react-router-dom";
import { itemLengthRequiredRule, requiredRule, itemUniqueBetweenRule } from "../../../../../utils/validators/general";
import { goIdentifierRule } from "../../../../../utils/validators/go";

const RelevantResourcesList = ({ form, fields, add, remove, resourceTypes, relevantResources, setRelevantResources, modelId }) => {
    const {
        token: { borderRadius, colorInfoBg },
    } = theme.useToken();

    const onResourceNameChanged = (i) => (e) =>
        setRelevantResources(relevantResources.map((relevantResource, index) => (i === index ? { ...relevantResource, name: e.target.value } : relevantResource)));

    const onResourceTypeChanged = (i) => (type) =>
        setRelevantResources(relevantResources.map((relevantResource, index) => (i === index ? { ...relevantResource, type } : relevantResource)));

    const resourceTypeOptions = resourceTypes.map((resourceType) => ({
        value: resourceType.id,
        label: resourceType.name,
    }));

    const getItems = (index) => () => (form.getFieldValue(["meta", "rel_resources"]) || []).filter((_, i) => i !== index);
    const getValue = (index) => () => form.getFieldValue(["meta", "rel_resources"])[index];
    const compare = (v, i) => v.name === i.name;

    const uniqueRule = (index) => itemUniqueBetweenRule(getValue(index), getItems(index), compare);

    return (
        <Space wrap={true}>
            {fields.map((field, i) => (
                <div style={{ paddingLeft: 5, paddingRight: 5, borderRadius, background: colorInfoBg }}>
                    <Row wrap align="middle" gutter={5}>
                        <Col>
                            <TinyFormItem {...field} name={[i, "name"]} rules={[requiredRule, goIdentifierRule, uniqueRule(i)]}>
                                <Input size="small" placeholder="Имя ресурса" onChange={onResourceNameChanged(i)} />
                            </TinyFormItem>
                        </Col>
                        <Col>
                            <TinyFormItem {...field} name={[i, "resource_type_id"]} rules={[requiredRule]}>
                                <Select size="small" options={resourceTypeOptions} placeholder="Тип ресурса" onSelect={onResourceTypeChanged(i)} />
                            </TinyFormItem>
                        </Col>
                        <Col>
                            <Link to={`/models/${modelId}/resource-types/${relevantResources[i]?.type}/edit`}>
                                <Button disabled={!relevantResources[i]?.type} icon={<EyeOutlined />} type="link" size="small" />
                            </Link>
                        </Col>
                        <Col>
                            <Button
                                danger
                                size="small"
                                icon={<CloseOutlined />}
                                onClick={() => {
                                    remove(i);
                                    setRelevantResources((relevantResources || []).filter((_, index) => index !== i));
                                }}
                            />
                        </Col>
                    </Row>
                </div>
            ))}
            <Button
                icon={<PlusOutlined />}
                size="small"
                onClick={() => {
                    add();
                    setRelevantResources([...relevantResources, {}]);
                }}
            />
        </Space>
    );
};

export default ({ form, resourceTypes, modelId, templates, funcs, ...formProps }) => {
    const [actualForm] = form ? [form] : Form.useForm();
    const [selectedType, setSelectedType] = useState(actualForm.getFieldValue(["meta", "type"]));

    const relResources = actualForm.getFieldValue(["meta", "rel_resources"]) || [];
    const [relevantResources, setRelevantResources] = useState(relResources.map((r) => ({ name: r?.name, type: r?.resource_type_id })));

    // useEffect(() => {
    //     setSelectedType();
    // }, [actualForm]);

    const bodyItems = {
        irregular_event: IrregularEventBody,
        operation: OperationBody,
        rule: RuleBody,
    };

    const SelectedBodyItem = selectedType ? bodyItems[selectedType] : () => <Typography.Text type="secondary">Укажите вид операции</Typography.Text>;

    const typeOptions = [
        { value: "irregular_event", label: "Нерегулярное событие" },
        { value: "operation", label: "Операция" },
        { value: "rule", label: "Правило" },
    ];

    const getItems = () => (templates || []).filter((item) => item.id !== actualForm.getFieldValue("id"));
    const getValue = () => actualForm.getFieldsValue();
    const compare = (v, i) => v.meta.name === i.meta.name;

    const uniqueRule = itemUniqueBetweenRule(getValue, getItems, compare);

    return (
        <Form form={actualForm} {...formProps}>
            <Form.Item hidden name={["meta", "id"]}>
                <InputNumber />
            </Form.Item>
            <Row gutter={10}>
                <Col flex={12}>
                    <Form.Item label="Название образца операции" name={["meta", "name"]} rules={[requiredRule, uniqueRule]}>
                        <Input placeholder="Укажите имя образца операции" />
                    </Form.Item>
                </Col>
                <Col flex={12}>
                    <Form.Item label="Вид" name={["meta", "type"]} rules={[requiredRule]}>
                        <Select options={typeOptions} onSelect={(value) => setSelectedType(value)} placeholder="Выберите вид операции" />
                    </Form.Item>
                </Col>
            </Row>
            <Form.Item label="Релевантные ресурсы" name="_check" rules={[itemLengthRequiredRule(actualForm, ["meta", "rel_resources"])]}>
                <Form.List name={["meta", "rel_resources"]}>
                    {(fields, { add, remove }) => (
                        <RelevantResourcesList
                            setRelevantResources={setRelevantResources}
                            relevantResources={relevantResources}
                            fields={fields}
                            add={add}
                            remove={remove}
                            resourceTypes={resourceTypes}
                            modelId={modelId}
                            form={actualForm}
                        />
                    )}
                </Form.List>
            </Form.Item>
            <Typography.Title level={5}>Тело образца</Typography.Title>
            <SelectedBodyItem relevantResources={relevantResources} form={actualForm} resourceTypes={resourceTypes} selectedType={selectedType} funcs={funcs}/>
        </Form>
    );
};
