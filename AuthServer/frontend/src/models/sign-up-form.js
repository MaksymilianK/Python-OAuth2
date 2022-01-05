import {ref} from "vue";

export class SignUpForm {
    constructor() {
        this.nick = ref("");
        this.email = ref("");
        this.password = ref("");
        this.repeatPassword = ref("");
    }
}