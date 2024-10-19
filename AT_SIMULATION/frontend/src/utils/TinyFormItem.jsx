import { Form } from "antd";
import styled from "styled-components";

const NoMGFormItem = styled(Form.Item)`
    margin-bottom: 0px;
    position: relative;
`;

const TinyFormItem = styled(NoMGFormItem)`
    .ant-form-item-explain {
        position: absolute;
        top: calc(100% - var(--ant-font-size)/2 - 1px);
        left: 5px;
        width: auto;
        max-width: calc(100% - 11px);
        display: flex;
        transition: 0.2s;
    }

    .ant-form-item-explain > div {
        position: relative;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        background: white;
        line-height: 1;
        transition: 0.2s;
        font-size: calc(var(--ant-font-size) - 1px);
        padding: 0px 2px;
    }

    .ant-form-item-explain > :first-child {
        flex-grow: 0;
        flex-shrink: 0;
        flex-basis: auto;
        max-width: 100%;
    }

    .ant-form-item-explain > *:not(:first-child) {
        flex-grow: 0;
        flex-shrink: 1;
    }
`;

export default TinyFormItem;
