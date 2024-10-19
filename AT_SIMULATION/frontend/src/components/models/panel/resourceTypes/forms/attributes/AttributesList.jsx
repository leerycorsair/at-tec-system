import { PlusOutlined } from "@ant-design/icons";
import { Button, Empty, Table } from "antd";
import { useState } from "react";
import { getColumns } from "./columns";
import "./AttributesList.css"

const AttributesFormList = ({ form, fields, add, remove }) => {
    const [selectedTypes, setSelectedTypes] = useState(
        Object.fromEntries(form.getFieldValue("attributes")?.map((attribute, i) => [i, attribute.type]) || [])
    );

    const [enumOptions, setEnumOptions] = useState(
        Object.fromEntries(
            form
                .getFieldValue("attributes")
                ?.map((attribute, i) => [i, attribute.type === "enum" ? attribute.enum_values_set : null]) || []
        )
    );

    const columns = getColumns({ form, enumOptions, setEnumOptions, selectedTypes, setSelectedTypes, remove });

    return !fields.length ? (
        <Empty description="Параметров не добавлено">
            <Button style={{ width: "100%" }} icon={<PlusOutlined />} onClick={() => add({})}>
                Добавить
            </Button>
        </Empty>
    ) : (
        <div>
            <div style={{ marginTop: 5 }}>
                <Table size="small" className="type-attributes-table" dataSource={fields} pagination={false} columns={columns} />
            </div>
            <Button style={{ width: "100%" }} icon={<PlusOutlined />} onClick={() => add({})}>
                Добавить
            </Button>
        </div>
    );
};

export default AttributesFormList;
