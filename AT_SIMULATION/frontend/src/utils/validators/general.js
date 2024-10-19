export const requiredRule = {
    required: true,
    message: "Заполните",
};

export const lengthRequiredRule = {
    validator: (_, value) => (value && value.length ? Promise.resolve() : Promise.reject(new Error("Укажите элементы"))),
};

export const lengthMinRequiredRule = (min) => ({
    validator: (_, value) => (value && value.length >= min ? Promise.resolve() : Promise.reject(new Error(`Минимум ${min} элемента`))),
});

export const itemLengthRequiredRule = (form, name) => ({
    validator: () => (form.getFieldValue(name) && form.getFieldValue(name).length ? Promise.resolve() : Promise.reject(new Error("Укажите элементы"))),
});

export const itemUniqueRule = (form, index, listName, compare = (v, i) => v === i) => ({
    validator: (_, value) => {
        const items = form.getFieldValue(listName);
        try {
            Array.from(items);
        } catch (e) {
            return Promise.reject(new Error("Некорректный элемент формы"));
        }
        if (!value || !items) {
            return Promise.resolve();
        }
        const duplicate = items.filter((item, idx) => compare(value, item) && idx !== index);
        if (duplicate.length > 0) {
            return Promise.reject(new Error("Укажите уникальное значение"));
        }
        return Promise.resolve();
    },
});

export const itemUniqueBetweenRule = (getValue, getListItems, compare = (v, i) => v === i) => ({
    validator: () => {
        const value = getValue();
        const listItems = getListItems();
        return listItems.filter((item) => compare(value, item)).length ? Promise.reject(new Error("Укажите уникальное значение")) : Promise.resolve();
    },
});
