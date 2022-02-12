export class UpdateTaskRequest {
    constructor(id, text, day, status) {
        this.id = id;
        this.text = text;
        this.day = day;
        this.status = status;
    }
}