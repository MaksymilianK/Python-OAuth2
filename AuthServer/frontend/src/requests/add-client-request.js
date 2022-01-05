export class AddClientRequest{
    constructor(name, description, redirectUrl) {
        this.name = name;
        this.description = description;
        this.redirectUrl = redirectUrl;
    }
}