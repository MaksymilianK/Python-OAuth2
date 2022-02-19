import {httpService} from "@/services/http-service";

export const scopeService = {

  async get_for_client(client_id) {
    return httpService.get(`/scopes/${client_id}`);
  },

  async get_all() {
    return httpService.get("/scopes");
  },

  revoke_for_client(client_id) {
    return httpService.post(`/scopes/${client_id}`);
  }
}
