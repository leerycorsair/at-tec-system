import { InputNumber, Select, Spin } from "antd";
import CheckboxItem from "../../../../../../utils/CheckboxItem";

const AttributeControl = ({ attribute, value, onChange }) => {
    const controlsTypesMapping = {
        int: {
            component: InputNumber,
            props: {
                value,
                onChange,
                placeholder: "Введите целочисленное значение",
                precision: 0,
                style: { width: "100%" },
            },
        },
        float: {
            component: InputNumber,
            props: {
                value,
                onChange,
                placeholder: "Введите числовое значение",
                style: { width: "100%" },
            },
        },
        bool: {
            component: CheckboxItem,
            props: {
                value,
                onChange,
                children: "Укажите логическое значение",
            },
        },
        enum: {
            component: Select,
            props: {
                value,
                onChange,
                options: (attribute?.enum_values_set || []).map((value) => ({ value })),
                style: { width: "100%" },
                placeholder: "Выберите значение",
            },
        },
    };
    if (!attribute) {
        return <Spin />
    }
    const ControlComponent = controlsTypesMapping[attribute.type].component;
    const props = controlsTypesMapping[attribute.type].props;

    return <ControlComponent {...props} />;
};

export default AttributeControl;