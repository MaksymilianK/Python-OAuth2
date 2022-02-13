export const noteValidators = {

    validateTitle(newTitle) {
        if (!(newTitle.length > 0)) {
            return "Title is empty!";
        }
        else if (!(newTitle.length <= 30)){
            return "Title max length is 30 chars!";
        }
        return "";
    },

    validateNote(newNote) {
        if (!(newNote.length > 0)) {
            return "Note is empty!";
        }
        else if (!(newNote.length <= 250)){
            return "Maximum note max length is 250 chars!";
        }
        return "";
    }
}
