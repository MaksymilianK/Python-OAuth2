export class AddClientRequest{
    constructor(name, description, redirectURL) {
        this.name = name;
        this.description = description;
        this.redirectURL = redirectURL;
    }
}