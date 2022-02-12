import {NewPublicationRequest} from "@/requests/new-publication-request";
import {httpService} from "@/services/http-service";
import {PublicationDeleteRequest} from "@/requests/note-delete-request";
import {EditPublicationRequest} from "@/requests/edit-publication-request";

export const publicationService = {
    addPublication(content) {
        const body = new NewPublicationRequest(
            content,
        );

        return httpService.post("/add-publication", body);
    },

    getPublications(){

        return httpService.get("/get-publications");
    },

    deletePublication(id){
        const body = new PublicationDeleteRequest(
            id,
        );

        return httpService.delete("/delete-publication", body);
    },

    editPublication(id, content) {
        const body = new EditPublicationRequest(
            id,
            content,
        );

        return httpService.put("/edit-publication", body);
    },
}