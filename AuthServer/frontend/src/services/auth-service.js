import {httpService} from "@/services/http-service";

export const authService = {

    authorize(authCodeRequest) {
        return httpService.post("/authorization", authCodeRequest)
    },

    redirectToClient(redirectUrl, code) {
        window.location.replace(`${redirectUrl}?code=${code}`);
    }
}