import {ref} from "vue";

export class ClientResponse {
    constructor() {
        this.id = ref(0);
        this.name = ref("");
        this.description = ref("");
        this.requestUrl = ref("");
    }

    setResponse(responseBody) {
        this.id.value = responseBody.id;
        this.name.value = responseBody.name;
        this.description.value = responseBody.description;
        this.requestUrl.value = responseBody.requestUrl;
    }
}