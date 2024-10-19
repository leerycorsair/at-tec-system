import { Row, Col, Input, Button, Empty, Form, Collapse, Table } from "antd";
import GoTypingInput from "../../../../../../utils/GoTypingInput";
import TinyFormItem from "../../../../../../utils/TinyFormItem";
import { useState } from "react";
import CodeEditorItem, { defaultEditorDidMount, defaultEditorOptions } from "../../../../../../utils/CodeEditorItem";
import { languages } from "monaco-editor";
import { MinusCircleOutlined, PlusOutlined } from "@ant-design/icons";
import { isValidGoIdentifier } from "../../../../../../utils/GoTypingInput";
import { requiredRule } from "../../../../../../utils/validators/general";
import { goIdentifierRule } from "../../../../../../utils/validators/go";

const ParametersList = ({ fields, parameters, setParameters, add, remove }) => {
    const handleParameterNameChanged = (index) => (e) => {
        const newParameters = [...parameters];
        newParameters[index] = { ...newParameters[index], name: e.target.value };
        setParameters(newParameters);
    };

    const handleParameterTypeChanged = (index) => (type) => {
        const newParameters = [...parameters];
        newParameters[index] = { ...newParameters[index], type };
        setParameters(newParameters);
    };

    const columns = [
        {
            key: "remove",
            render: (field, _, index) => (
                <Button
                    icon={<MinusCircleOutlined />}
                    type="link"
                    size="small"
                    onClick={() => {
                        remove(index);
                        setParameters(parameters.filter((_, i) => i !== index));
                    }}
                />
            ),
        },
        {
            key: "name",
            title: "Имя параметра",
            render: (field, _, index) => (
                <TinyFormItem {...field} name={[index, "name"]} rules={[requiredRule, goIdentifierRule]}>
                    <Input placeholder="Имя аргумента" onChange={handleParameterNameChanged(index)} />
                </TinyFormItem>
            ),
        },
        {
            key: "type",
            title: "Тип параметра",
            render: (field, _, index) => (
                <TinyFormItem {...field} name={[index, "type"]} rules={[requiredRule]}>
                    <GoTypingInput placeholder="Тип аргумента" onChange={handleParameterTypeChanged(index)} />
                </TinyFormItem>
            ),
        },
    ];

    return (
        <>
            {fields.length ? <Table size="small" columns={columns} dataSource={fields} pagination={false} /> : <Empty description="Параметров не добавлено" />}
            <div style={{ marginTop: 5 }}>
                <Button
                    style={{ width: "100%" }}
                    icon={<PlusOutlined />}
                    onClick={() => {
                        add({});
                        setParameters([...parameters, {}]);
                    }}
                >
                    Добавить
                </Button>
            </div>
        </>
    );
};

export default ({ form, funcs }) => {
    const [parameters, setParameters] = useState(form.getFieldValue("params") || []);

    const paramsItem = {
        key: "params",
        label: "Параметры",
        children: (
            <TinyFormItem>
                <Form.List name="params">
                    {(fields, { add, remove }) => <ParametersList fields={fields} parameters={parameters} setParameters={setParameters} add={add} remove={remove} />}
                </Form.List>
            </TinyFormItem>
        ),
    };

    const autoComplete = (model, position) => {
        const word = model.getWordAtPosition(position);

        const filteredParameters = (parameters || []).filter((param) => param?.name && isValidGoIdentifier(param.name) && param.name.includes(word?.word || word));

        const suggestions = filteredParameters.map((param) => ({
            label: param.name,
            kind: languages.CompletionItemKind.Variable,
            insertText: param.name,
            detail: "Параметр функции",
        }));

        const filteredFuncs = (funcs || []).filter((func) => func?.name && isValidGoIdentifier(func.name) && func.name.includes(word?.word || word));

        const funcSuggestions = filteredFuncs.map((func) => ({
            label: func.name,
            kind: languages.CompletionItemKind.Function,
            insertText: func.name,
            detail: "Функция",
        }));

        return suggestions.concat(funcSuggestions);
    };
    const editorDidMount = defaultEditorDidMount;
    const codeEditorOptions = defaultEditorOptions;

    const bodyItem = {
        key: "body",
        label: "Тело функции",
        children: (
            <TinyFormItem name="body" rules={[requiredRule]}>
                <CodeEditorItem language="go" options={codeEditorOptions} height="270px" autoComplete={autoComplete} editorDidMount={editorDidMount} />
            </TinyFormItem>
        ),
    };

    return (
        <Row gutter={[5, 5]}>
            <Col flex={9} style={{ maxWidth: "37.5%" }}>
                <Collapse size="small" defaultActiveKey="params" items={[paramsItem]} />
            </Col>
            <Col flex={15} style={{ maxWidth: "62.5%" }}>
                <Collapse size="small" defaultActiveKey="body" items={[bodyItem]} />
            </Col>
        </Row>
    );
};
