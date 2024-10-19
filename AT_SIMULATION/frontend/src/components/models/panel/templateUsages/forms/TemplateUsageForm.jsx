import { EditOutlined } from "@ant-design/icons";
import { Col, Form, Input, Row, Select, Button, Empty } from "antd";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import ResourcesFormList from "./resources/ResourcesList";
import { requiredRule, itemUniqueBetweenRule } from "../../../../../utils/validators/general";
import { goIdentifierRule } from "../../../../../utils/validators/go";

const TemplateSelect = ({ value, onChange, templates, onSelect, modelId }) => {
    const template = templates ? templates.find((t) => t.meta.id === value) : undefined;
    return (
        <Row>
            <Col flex="auto">
                <Select
                    value={value}
                    onChange={onChange}
                    placeholder="Выберите образец"
                    options={templates.map((template) => ({
                        key: template.meta.id.toString(),
                        label: template.meta.name,
                        value: template.meta.id,
                    }))}
                    onSelect={onSelect}
                />
            </Col>
            <Col>
                <Link to={`/models/${modelId}/templates/${value}/edit`}>
                    <Button disabled={!template} icon={<EditOutlined />} type="link">
                        Редактировать
                    </Button>
                </Link>
            </Col>
        </Row>
    );
};

export default ({ form, resources, templates, modelId, templateUsages, ...formProps }) => {
    const [actualForm] = form ? [form] : Form.useForm();
    const [selectedTemplate, setSelectedTemplate] = useState(actualForm.getFieldValue("template_id"));

    const template = templates.find((tpl) => tpl.meta.id === selectedTemplate);

    useEffect(() => {
        const getOrClearOldResource = (resource_id, rel_resource_index) => {
            if (!resource_id) {
                return;
            }
            const resource = resources.find((res) => res.id === resource_id);
            const relResource = (template?.meta?.rel_resources || [])[rel_resource_index];

            if (!relResource || !resource) {
                return;
            }

            if (relResource.resource_type_id === resource.resource_type_id) {
                return resource_id;
            }
        };

        const oldRelevantResources = actualForm.getFieldValue("arguments") || [];
        if (template && template.meta.rel_resources) {
            actualForm.setFieldValue(
                "arguments",
                template.meta.rel_resources.map((rel_resource, i) => ({
                    relevant_resource_id: rel_resource.id,
                    resource_id: getOrClearOldResource(oldRelevantResources[i]?.resource_id, i),
                }))
            );
        }
    }, [templates, template]);

    const getItems = () => (templateUsages || []).filter(item => item.id !== actualForm.getFieldValue("id"))
    const getValue = () => actualForm.getFieldsValue()
    const compare = (v, i) => v.name === i.name;

    const uniqueRule = itemUniqueBetweenRule(getValue, getItems, compare)

    return (
        <Form form={actualForm} {...formProps}>
            <Form.Item name="id" hidden />
            <Form.Item name="model_id" hidden />
            <Form.Item name="name" label="Имя операции" rules={[requiredRule, goIdentifierRule, uniqueRule]}>
                <Input placeholder="Укажите имя операции" />
            </Form.Item>
            <Form.Item name="template_id" label="Образец" rules={[requiredRule]}>
                <TemplateSelect templates={templates} modelId={modelId} onSelect={setSelectedTemplate} />
            </Form.Item>
            <Form.Item label="Релевантные ресурсы">
                {selectedTemplate ? (
                    <Form.List name="arguments">
                        {(fields) => (
                            <ResourcesFormList
                                modelId={modelId}
                                fields={fields}
                                template={template}
                                resources={resources}
                            />
                        )}
                    </Form.List>
                ) : (
                    <Empty description="Выберите образец операции" />
                )}
            </Form.Item>
        </Form>
    );
};
