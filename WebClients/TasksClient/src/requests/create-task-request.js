export class CreateTaskRequest {
    constructor(text, day) {
        this.text = text;
        this.day = day;
        this.status = false;
    }
}