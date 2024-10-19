import MonacoEditor from "@uiw/react-monacoeditor";
import { Spin } from "antd";
import { useState, useEffect } from "react";

export const defaultEditorBackground = "#e9e9ff";
export const defaultEditorSidersBackground = "#d8d8ed";
export const defaultEditorDidMount = (_, monaco) => {
    monaco.editor.defineTheme("at-sym", {
        base: "vs",
        inherit: true,
        rules: [],
        colors: {
            "editor.background": defaultEditorBackground,
            "scrollbarSlider.background": defaultEditorSidersBackground,
            "editorGutter.background": defaultEditorSidersBackground,
        },
    });
};

export const defaultEditorOptions = {
    selectOnLineNumbers: true,
    roundedSelection: false,
    readOnly: false,
    cursorStyle: "line",
    automaticLayout: false,
    theme: "at-sym",
    scrollbar: {
        useShadows: true,
        verticalHasArrows: true,
        horizontalHasArrows: true,
        vertical: "visible",
        horizontal: "visible",
        verticalScrollbarSize: 17,
        horizontalScrollbarSize: 17,
        arrowSize: 30,
    },
    suggest: {
        showFields: false,
    },
};

const CodeEditorItem = ({
    value,
    onChange,
    onCodeChanged,
    language,
    options,
    height,
    autoComplete,
    editorDidMount,
}) => {
    const [code, setCode] = useState(value);
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        setMounted(true);
    }, [])

    useEffect(() => {
        try {
            onChange(code);
        } catch (e) {}
        try {
            onCodeChanged(code);
        } catch (e) {}
    }, [code]);

    const handleEditorDidMount = (editor, monaco) => {
        if (value) {
            setTimeout(() => editor.setValue(value), 500);
        }
        try {
            return editorDidMount(editor, monaco);
        } catch (e) {}
    };

    return (
        mounted ? <MonacoEditor
            onChange={setCode}
            language={language}
            options={options}
            height={height}
            defaultValue={value}
            autoComplete={autoComplete}
            editorDidMount={handleEditorDidMount}
            style={{ width: "100%" }}
        /> : <Spin />
    );
};

export default CodeEditorItem;
