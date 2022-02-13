export const publicationValidators = {

    validatePublication(Publication) {
        if (!(Publication.length > 0)) {
            return "Publication is empty!";
        }
        else if (!(Publication.length <= 250)){
            return "Maximum publication length is 250 chars!";
        }
        return "";
    }
}
