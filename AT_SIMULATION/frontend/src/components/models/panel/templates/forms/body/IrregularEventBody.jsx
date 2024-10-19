import { useEffect, useState } from "react";

import { Row, Col, Form, Select, InputNumber, Collapse } from "antd";
import CodeEditorItem, { defaultEditorDidMount, defaultEditorOptions } from "../../../../../../utils/CodeEditorItem";
import { makeAutoComplete } from "./autoComplete";
import TinyFormItem from "../../../../../../utils/TinyFormItem";
import { requiredRule } from "../../../../../../utils/validators/general";
// import {} from "monaco-editor/esm/vs/editor/browser/services/editorWorkerService";

export default ({ form, relevantResources, resourceTypes, selectedType, funcs }) => {

    const options = [
        { value: "normal", label: "Нормальное распределение" },
        { value: "precise", label: "Точное число" },
        { value: "random", label: "Случайное число" },
        { value: "uniform", label: "Равномерное распределение" },
        { value: "exponential", label: "Экспоненциальное распределение" },
        { value: "gaussian", label: "Распределение Гаусса" },
        { value: "poisson", label: "Распределение Пуассона" },
    ];

    const [selectedGeneratorType, setSelectedGeneratorType] = useState(form.getFieldValue(["generator", "type"]));

    useEffect(() => {
        if (selectedGeneratorType === "precise") {
            form.setFieldValue(["generator", "dispersion"], 0);
        }
    }, [selectedGeneratorType]);

    useEffect(() => {
        setSelectedGeneratorType(form.getFieldValue(["generator", "type"]));
    }, [selectedType]);

    const editorDidMount = defaultEditorDidMount;
    const codeEditorOptions = defaultEditorOptions;
    const autoComplete = makeAutoComplete(relevantResources, resourceTypes, funcs);

    const generatorItem = {
        key: "generator",
        label: "Генератор события",
        children: [
            <Form.Item label="Тип генератора" name={["generator", "type"]} rules={[requiredRule]}>
                <Select placeholder="Укажите тип генератора" options={options} onSelect={(value) => setSelectedGeneratorType(value)} />
            </Form.Item>,
            <Form.Item label="Мат. ожидание" name={["generator", "value"]} rules={[requiredRule]}>
                <InputNumber style={{ width: "100%" }} placeholder="Укажите мат. ожидание" />
            </Form.Item>,
            <Form.Item label="Дисперсия" name={["generator", "dispersion"]} rules={[requiredRule]}>
                <InputNumber style={{ width: "100%" }} disabled={selectedGeneratorType === "precise"} placeholder="Укажите диперсию" />
            </Form.Item>,
        ],
    };

    const bodyItem = {
        key: "body",
        label: "Действия (тело события)",
        children: (
            <TinyFormItem name={["body", "body"]} rules={[requiredRule]}>
                <CodeEditorItem language="go" options={codeEditorOptions} height="258px" autoComplete={autoComplete} editorDidMount={editorDidMount} />
            </TinyFormItem>
        ),
    };

    return (
        <Row gutter={5}>
            <Col style={{ minWidth: 315 }}>
                <Collapse size="small" defaultActiveKey="generator" items={[generatorItem]} />
            </Col>
            <Col flex="auto">
                <Collapse size="small" defaultActiveKey="body" items={[bodyItem]} />
            </Col>
        </Row>
    );
};
