import {httpService} from "@/services/http-service";
import {SignInRequest} from "@/requests/sign-in-request";
import {SignUpRequest} from "@/requests/sign-up-request";
import {HTTP_NO_CONTENT, HTTP_OK} from "@/utils/http-status";
import {ref} from "vue";

export const userService = {

    _current: ref(""),

    get current() {
        return this._current;
    },

    get_current() {
        return httpService.get("/current-user")
            .then(res => this._try_set_current(res));
    },

    signUp(formModel) {
        const body = new SignUpRequest(formModel.nick.value, formModel.email.value, formModel.password.value);
        return httpService.post("/users", body)
            .then(res => this._try_set_current(res));
    },

    signIn(formModel) {
        const body = new SignInRequest(formModel.email.value, formModel.password.value);
        return httpService.post("/current-user", body)
            .then(res => this._try_set_current(res));
    },

    signOut() {
        return httpService.delete("/current-user")
            .then(res => this._try_unset_current(res));
    },

    _try_set_current(res) {
        if (res.status === HTTP_OK) {
            this._current.value = res.body.nick;
        }
        return res;
    },

    _try_unset_current(res) {
        if (res.status === HTTP_NO_CONTENT) {
            this._current.value = "";
        }
        return res;
    }
}
