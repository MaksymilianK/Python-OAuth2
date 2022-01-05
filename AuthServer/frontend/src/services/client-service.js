import {httpService} from "@/services/http-service";
import {AddClientRequest} from "@/requests/add-client-request";

export const clientService = {
    add(formModel) {
        const body = new AddClientRequest(
            formModel.name.value,
            formModel.description.value,
            formModel.redirectURL.value
        );

        return httpService.post("/clients", body);
    }
}
