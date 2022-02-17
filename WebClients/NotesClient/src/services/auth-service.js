import {ref} from "vue";
import {httpService} from "@/services/http-service";
import {authServerUrlBackend} from "@/config";
import {TokenRevocationRequest} from "@/requests/token-revocation-request";
import {HTTP_NO_CONTENT, HTTP_OK} from "@/utils/http-status";
import {TokenRequest} from "@/requests/token-request";
import {HTTP_UNAUTHORIZED} from "../utils/http-status";

const CURRENT_KEY = "NOTES_AUTH_USER";
const TOKEN_KEY = "NOTES_AUTH_TOKEN";

export const authService = {

    _current: ref(localStorage.getItem(CURRENT_KEY)),
    _token: localStorage.getItem(TOKEN_KEY),

    get current() {
        return this._current;
    },

    get token() {
        return this._token;
    },

    revokeToken() {
        return httpService.post(`${authServerUrlBackend}/token-revocation`, new TokenRevocationRequest(this._token), true)
            .then(res => {
                if (res.status === HTTP_NO_CONTENT) {
                    localStorage.removeItem(CURRENT_KEY);
                    localStorage.removeItem(TOKEN_KEY);
                    this._current.value = null;
                    this._token = null;
                }
                return res;
            });
    },

    get_token(code) {
        return httpService.post(`${authServerUrlBackend}/auth-token`, new TokenRequest(code), true)
            .then(res => {
                if (res.status === HTTP_OK) {
                    localStorage.setItem(CURRENT_KEY, res.body.owner);
                    localStorage.setItem(TOKEN_KEY, res.body.token);
                    this._current.value = res.body.owner;
                    this._token = res.body.token;
                }
                return res;
            });
    },

    check_auth() {
        if (!this.token) return;

        return httpService.post(`${authServerUrlBackend}/token-info`, {token: this.token}, true)
            .then(res => {
                if (res.status === HTTP_UNAUTHORIZED) {
                    localStorage.removeItem(CURRENT_KEY);
                    localStorage.removeItem(TOKEN_KEY);
                    this._current.value = null;
                    this._token = null;
                }
            });
    }
}
