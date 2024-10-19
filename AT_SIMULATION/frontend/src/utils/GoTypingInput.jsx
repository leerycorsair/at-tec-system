import { AutoComplete } from "antd";

export const goIdentifierRegexp = /^([a-zA-Zа-яА-Я_](\w|[а-яА-Я])*)$/

export const isValidGoIdentifier = (name) => {
    return goIdentifierRegexp.test(name);
};

const options = [
    "int",
    "int8",
    "int16",
    "int32",
    "int64",
    "uint",
    "uint8",
    "uint16",
    "uint32",
    "uint64",
    "uintptr",
    "float32",
    "float64",
    "complex64",
    "complex128",
    "string",
    "rune",
    "bool",
    "map",
].map((value) => ({ value }));

export default (props) => <AutoComplete {...props} options={options} />;
