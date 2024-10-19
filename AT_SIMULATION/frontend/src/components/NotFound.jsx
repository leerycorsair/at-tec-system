import { Result } from "antd";
import { Link } from "react-router-dom";

export default () => <Result status="warning" title="Страница не найдена" extra={<Link to="/">На главную</Link>} />;
