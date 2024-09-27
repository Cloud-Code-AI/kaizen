"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.StorageManager = void 0;
class StorageManager {
    context;
    constructor(context) {
        this.context = context;
    }
    getValue(key) {
        return this.context.globalState.get(key);
    }
    setValue(key, value) {
        this.context.globalState.update(key, value);
    }
}
exports.StorageManager = StorageManager;
//# sourceMappingURL=storageManager.js.map