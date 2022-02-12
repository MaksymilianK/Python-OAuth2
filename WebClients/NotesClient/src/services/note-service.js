import {NewNoteRequest} from "@/requests/new-note-request";
import {httpService} from "@/services/http-service";
import {NoteDeleteRequest} from "@/requests/note-delete-request";

export const noteService = {
    addNote(title, content) {
        const body = new NewNoteRequest(
            title,
            content,
        );

        return httpService.post("/add-note", body);
    },

    getNotes(){

        return httpService.get("/get-notes");
    },

    deleteNote(id){
        const body = new NoteDeleteRequest(
            id,
        );

        return httpService.delete("/delete-note", body);
    },
}