import {ref} from "vue";
import {httpService} from "@/services/http-service";
import {authServerUrlBackend} from "@/config";
import {TokenRevocationRequest} from "@/requests/token-revocation-request";
import {HTTP_NO_CONTENT, HTTP_OK} from "@/utils/http-status";
import {TokenRequest} from "@/requests/token-request";

const CURRENT_KEY = "AUTH_USER2";
const TOKEN_KEY = "AUTH_TOKEN2";

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
        return httpService.post(`${authServerUrlBackend}/api/token-revocation`, new TokenRevocationRequest(this._token), true)
            .then(res => {
                if (res.status === HTTP_NO_CONTENT) {
                    localStorage.clear();
                    this._current.value = null;
                    this._token = null;
                }
                return res;
            });
    },

    get_token(code) {
        return httpService.post(`${authServerUrlBackend}/api/auth-token`, new TokenRequest(code), true)
            .then(res => {
                if (res.status === HTTP_OK) {
                    localStorage.setItem(CURRENT_KEY, res.body.owner);
                    localStorage.setItem(TOKEN_KEY, res.body.token);
                    this._current.value = res.body.owner;
                    this._token = res.body.token;
                }
                return res;
            });
    }
}
