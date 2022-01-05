import {ref} from "vue";

export class SignInForm {
    constructor() {
        this.email = ref("");
        this.password = ref("");
    }
}