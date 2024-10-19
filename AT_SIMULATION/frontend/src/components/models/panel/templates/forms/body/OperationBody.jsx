import { Row, Col, Form, InputNumber, Collapse } from "antd";
import CodeEditorItem, { defaultEditorDidMount, defaultEditorOptions } from "../../../../../../utils/CodeEditorItem";
import { makeAutoComplete } from "./autoComplete";
import TinyFormItem from "../../../../../../utils/TinyFormItem";
import { requiredRule } from "../../../../../../utils/validators/general";
// import {} from "monaco-editor/esm/vs/editor/browser/services/editorWorkerService";

export default ({ relevantResources, resourceTypes, funcs }) => {

    const editorDidMount = defaultEditorDidMount;
    const codeEditorOptions = defaultEditorOptions;

    const autoComplete = makeAutoComplete(relevantResources, resourceTypes, funcs);

    const conditionItem = {
        key: "condition",
        label: "Предусловие",
        children: (
            <TinyFormItem name={["body", "condition"]} rules={[requiredRule]}>
                <CodeEditorItem
                    language="go"
                    options={codeEditorOptions}
                    height="75px"
                    autoComplete={autoComplete}
                    editorDidMount={editorDidMount}
                />
            </TinyFormItem>
        ),
    };

    const bodyBeforeItem = {
        key: "body_before",
        label: "Действия в начале",
        children: (
            <TinyFormItem name={["body", "body_before"]} rules={[requiredRule]}>
                <CodeEditorItem
                    language="go"
                    options={codeEditorOptions}
                    height="200px"
                    // autoComplete={autoComplete}
                    editorDidMount={editorDidMount}
                />
            </TinyFormItem>
        ),
    };

    const bodyAfterItem = {
        key: "body_after",
        label: "Действия в конце",
        children: (
            <TinyFormItem name={["body", "body_after"]} rules={[requiredRule]}>
                <CodeEditorItem
                    language="go"
                    options={codeEditorOptions}
                    height="200px"
                    // autoComplete={autoComplete}
                    editorDidMount={editorDidMount}
                />
            </TinyFormItem>
        ),
    };

    return (
        <div>
            <Form.Item labelCol={6} layout="horizontal" name={["body", "delay"]} label="Длительность" rules={[requiredRule]}>
                <InputNumber style={{width: "100%"}} placeholder="Укажите длительность" />
            </Form.Item>
            <Row gutter={[5, 5]}>
                <Col span={24}>
                    <Collapse size="small" defaultActiveKey="condition" items={[conditionItem]} />
                </Col>
                <Col flex={12} style={{ maxWidth: "50%" }}>
                    <Collapse size="small" defaultActiveKey="body_before" items={[bodyBeforeItem]} />
                </Col>
                <Col flex={12} style={{ maxWidth: "50%" }}>
                    <Collapse size="small" defaultActiveKey="body_after" items={[bodyAfterItem]} />
                </Col>
            </Row>
        </div>
    );
};
