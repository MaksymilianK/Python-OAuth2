import {ref} from "vue/dist/vue";

export class AddClientForm {
    constructor() {
        this.name = ref("");
        this.description = ref("");
        this.redirectURL = ref("")
    }
}