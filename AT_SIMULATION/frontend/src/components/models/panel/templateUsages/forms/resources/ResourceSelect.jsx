import { EditOutlined } from "@ant-design/icons";
import { Button, Row, Col, Select } from "antd";
import { Link } from "react-router-dom";

const ResourceSelect = ({ value, onChange, resources, onSelect, modelId }) => {
    const resource = resources ? resources.find((r) => r.id === value) : undefined;
    return (
        <Row>
            <Col flex="auto">
                <Select
                    value={value}
                    onChange={onChange}
                    placeholder="Выберите ресурс ИМ"
                    options={resources.map((resource) => ({
                        value: resource.id,
                        label: resource.name,
                    }))}
                    onSelect={onSelect}
                />
            </Col>
            <Col>
                <Link to={`/models/${modelId}/resources/${value}/edit`}>
                    <Button disabled={!resource} icon={<EditOutlined />} type="link">
                        Редактировать
                    </Button>
                </Link>
            </Col>
        </Row>
    );
};


export default ResourceSelect