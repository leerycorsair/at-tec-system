import { Typography, Form, Tag } from "antd";
import AttributeControl from "./controls";
import TinyFormItem from "../../../../../../utils/TinyFormItem";

export const typeLabels = { int: "Целочисленный", float: "Численный", bool: "Логический", enum: "Перечислимый" };

export const getCollumns = ({ resourceType }) => {
    return [
        {
            key: 1,
            title: "Имя параметра",
            render: (field, _, i) => <Typography.Text>{resourceType.attributes[i]?.name}</Typography.Text>,
        },
        {
            key: 2,
            title: "Тип параметра",
            render: (field, _, i) => (
                <>
                    <Form.Item hidden name={[i, "rta_id"]} />
                    <Tag>{typeLabels[resourceType.attributes[i]?.type]}</Tag>
                </>
            ),
        },
        {
            key: 3,
            title: "Инициализируемое значение",
            render: (field, _, i) => (
                <TinyFormItem name={[i, "value"]}>
                    <AttributeControl attribute={resourceType.attributes[i]} />
                </TinyFormItem>
            ),
        },
    ];
};
