import { isValidGoIdentifier } from "../GoTypingInput";

export const goIdentifierRule = {
    validator: (_, value) => (isValidGoIdentifier(value) ? Promise.resolve() : Promise.reject(new Error("Неверный формат"))),
};
