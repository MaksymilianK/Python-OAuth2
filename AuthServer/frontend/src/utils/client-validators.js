export const clientValidators = {

    validateName(nick) {
        if (!nameRegex.test(nick)) {
            return "Name's length must be between 3 and 16 and must consist only of letters, numbers and underscores!";
        }
        return "";
    },

    validateDescription(description) {
        if (description.length < 10 || description.length > 250) {
            return "Description's length must be between 10 and 250!";
        }
        return "";
    },

    validateRedirectURL(redirectURL) {
        if (!redirectURL) {
            return "Redirect URL must not be empty!";
        }
        return "";
    }
}

const nameRegex = /^\w{3,16}$/;
