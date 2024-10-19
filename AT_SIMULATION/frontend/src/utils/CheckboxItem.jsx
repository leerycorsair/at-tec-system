import { Checkbox } from "antd";

export default ({ value, onChange, ...props }) => <Checkbox checked={value} onChange={(e) => onChange(e.target.checked)} {...props}/>;
