import { httpService } from "./http-service";
import { CreateTaskRequest } from "../requests/create-task-request";
import { UpdateTaskRequest } from "../requests/update-task-request";

export const taskService = {
    createTask(text, day) {
        return httpService.post('/tasks', new CreateTaskRequest(text, day));
    },
    deleteTask(id) {
        return httpService.delete(`/tasks/${id}`);
    },
    getTasks() {
        return httpService.get('/tasks');
    },
    getTask(id) {
        return httpService.get(`/tasks/${id}`);
    },
    updateTaskStatus(id, text, day, status) {
        return httpService.put(`/tasks/${id}`, new UpdateTaskRequest(id, text, day, status));
    }
}