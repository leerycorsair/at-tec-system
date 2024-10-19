import { getCollumns } from "./columns";
import { Empty, Table } from "antd";

const AttributesFormList = ({ fields, form, resourceType }) => {
    const collumns = getCollumns({ resourceType });
    return !fields.length ? (
        <Empty description="Параметров не добавлено" />
    ) : (
        <div style={{ marginTop: 5 }}>
            <Table size="small" dataSource={fields} pagination={false} columns={collumns} />
        </div>
    );
};

export default AttributesFormList