import { languages } from "monaco-editor";
import { goIdentifierRegexp, isValidGoIdentifier } from "../../../../../../utils/GoTypingInput";

export const makeAutoComplete = (relevantResources, resourceTypes, funcs) => (model, position) => {
    const word = model.getWordAtPosition(position);
    const lineContent = model.getLineContent(position.lineNumber);

    const textUntilPosition = lineContent.slice(0, position.column - 1);
    const splitByDot = textUntilPosition.split(".");

    if (splitByDot.length > 1) {
        const afterDot = splitByDot[splitByDot.length - 1].trim();

        const beforeDot = splitByDot[splitByDot.length - 2].trim();

        if (isValidGoIdentifier(afterDot) || afterDot === "") {
            const beforeDotMatch = beforeDot.match(goIdentifierRegexp);
            const validIdentifier = beforeDotMatch ? beforeDotMatch[0] : null;
            const resource = relevantResources.find((res) => res.name === validIdentifier);

            if (resource) {
                const resourceType = resourceTypes.find((type) => type.id === resource.type);
                if (resourceType) {
                    const suggestions = resourceType.attributes
                        .filter((attr) => attr.name.startsWith(afterDot))
                        .map((attr) => ({
                            label: attr.name,
                            kind: languages.CompletionItemKind.Property,
                            insertText: attr.name,
                            detail: `Параметр типа ресурса ${resourceType.name}`,
                        }));
                    return suggestions;
                }
            }
        }
    }

    const filteredResources = relevantResources.filter((resource) => resource?.name && isValidGoIdentifier(resource.name) && resource.name.includes(word?.word || word));

    const suggestions = filteredResources.map((resource) => ({
        label: resource.name,
        kind: languages.CompletionItemKind.Class,
        insertText: resource.name,
        detail: "Релевантный ресурс",
    }));

    const filteredFuncs = (funcs || []).filter((func) => func?.name && isValidGoIdentifier(func.name) && func.name.includes(word?.word || word));

    const funcSuggestions = filteredFuncs.map((func) => ({
        label: func.name,
        kind: languages.CompletionItemKind.Function,
        insertText: func.name,
        detail: "Функция",
    }));

    return suggestions.concat(funcSuggestions);
};
