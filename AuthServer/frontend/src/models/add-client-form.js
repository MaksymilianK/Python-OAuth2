import {ref} from "vue";

export class AddClientForm {
    constructor() {
        this.name = ref("");
        this.description = ref("");
        this.redirectUrl = ref("")
    }
}