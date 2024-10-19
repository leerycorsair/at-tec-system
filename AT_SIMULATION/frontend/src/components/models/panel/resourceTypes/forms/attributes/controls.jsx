import { InputNumber, Select } from "antd";
import CheckboxItem from "../../../../../../utils/CheckboxItem";

export const getControlsTypesMapping = ({ enumOptions }) => ({
    int: {
        component: InputNumber,
        getProps: () => ({
            placeholder: "Введите целочисленное значение",
            style: { width: "100%" },
            precision: 0,
            
        }),
    },
    float: {
        component: InputNumber,
        getProps: () => ({
            placeholder: "Введите числовое значение",
            style: { width: "100%" },
            
        }),
    },
    bool: {
        component: CheckboxItem,
        getProps: () => ({
            children: "Укажите логическое значение",
            style: { marginLeft: 7 },
        }),
    },
    enum: {
        component: Select,
        getProps: (i) => ({
            style: { width: "100%" },
            placeholder: "Выберите значение из набора",
            options: (enumOptions[i] || []).map((value) => ({ value })),
            
        }),
    },
});
