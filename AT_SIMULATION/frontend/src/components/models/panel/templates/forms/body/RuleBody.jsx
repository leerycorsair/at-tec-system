import { theme, Row, Col, Collapse } from "antd";
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
                <CodeEditorItem language="go" options={codeEditorOptions} height="250px" autoComplete={autoComplete} editorDidMount={editorDidMount} />
            </TinyFormItem>
        ),
    };

    const bodyItem = {
        key: "body",
        label: "Действия",
        children: (
            <TinyFormItem name={["body", "body"]} rules={[requiredRule]}>
                <CodeEditorItem
                    language="go"
                    options={codeEditorOptions}
                    height="250px"
                    // autoComplete={autoComplete}
                    editorDidMount={editorDidMount}
                />
            </TinyFormItem>
        ),
    };

    return (
        <Row gutter={[5, 5]}>
            <Col flex={9} style={{ maxWidth: "37.5%" }}>
                <Collapse size="small" defaultActiveKey="condition" items={[conditionItem]} />
            </Col>
            <Col flex={15} style={{ maxWidth: "62.5%" }}>
                <Collapse size="small" defaultActiveKey="body" items={[bodyItem]} />
            </Col>
        </Row>
    );
};
