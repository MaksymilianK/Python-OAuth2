export const noteValidators = {

    validateTitle(newTitle) {
        if (!(newTitle.length > 0)) {
            return "Title is empty!";
        }
        return "";
    },

    validateNote(newNote) {
        if (!(newNote.length > 0)) {
            return "Note is empty!";
        }
        else if (!(newNote.length < 250)){
            return "Maximum note length is 250 chars!";
        }
        return "";
    }
}