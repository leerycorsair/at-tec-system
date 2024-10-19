import { Table, Typography, Form, InputNumber } from "antd";
import TinyFormItem from "../../../../../../utils/TinyFormItem";
import ResourceSelect from "./ResourceSelect";
import { requiredRule } from "../../../../../../utils/validators/general";

const ResourcesFormList = ({ fields, resources, template, modelId }) => {
    const relevantResources = template?.meta?.rel_resources || [];
    const collumns = [
        {
            title: "Релевантный ресурс образца",
            key: "relevant_resource",
            render: (field, _, i) => (
                <>
                    <Form.Item {...field} name={[i, "relevant_resource_id"]} hidden>
                        <InputNumber value={relevantResources[i]?.id} />
                    </Form.Item>
                    <Typography.Text code>{relevantResources[i]?.name}</Typography.Text>
                </>
            ),
        },
        {
            title: "Реурс ИМ",
            key: "resource",
            render: (field, _, i) => (
                <TinyFormItem {...field} name={[i, "resource_id"]} rules={[requiredRule]}>
                    <ResourceSelect resources={resources.filter((res) => res.resource_type_id === relevantResources[i]?.resource_type_id)} modelId={modelId} />
                </TinyFormItem>
            ),
        },
    ];

    return <Table sticky columns={collumns} dataSource={fields} pagination={false} size="small" />;
};

export default ResourcesFormList;
