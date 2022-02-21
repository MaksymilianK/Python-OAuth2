<template>
  <p v-if="current" class="login-status">
      Status: zalogowany
    </p>
    <p v-else class="login-status">
      Status: niezalogowany
    </p>
  <div v-if="current" class="container">
    <Subheader @toggle-add-task="toggleAddTask" title="Task Tracker" :show-add-task="showAddTask" />
    <AddTask v-show="showAddTask" @add-task="addTask" />
    <Tasks @toggle-status="toggleStatus" @delete-task="deleteTask" :tasks="tasks" />
  </div>
</template>

<script>
import Subheader from "../components/Subheader";
import AddTask from "../components/AddTask";
import Tasks from "../components/Tasks";
import { ref } from "vue";
import { authService } from "@/services/auth-service";
import { taskService } from "@/services/task-service";
import { HTTP_201_CREATED, HTTP_OK, HTTP_NO_CONTENT, HTTP_UNAUTHORIZED, HTTP_FORBIDDEN } from "@/utils/http-status";

export default {
  name: "Home",
  components: {
    Tasks,
    AddTask,
    Subheader
  },
  setup() {
    const error = ref("");

    return {
      current: authService.current,
      error
    }
  },
  data() {
    return {
      tasks: [],
      showAddTask: false
    }
  },
  created() {
    this.fetchTasks();
  },
  methods: {
    toggleAddTask() {
      this.showAddTask = !this.showAddTask
    },
    addTask(task) {
      taskService.createTask(task.text, task.day)
          .then(res => {
            switch (res.status) {
              case HTTP_201_CREATED:
                this._addTask(res);
                break;
              case HTTP_UNAUTHORIZED:
              case HTTP_FORBIDDEN:
                window.location.replace(authService.getAuthUrl());
                break;
              default:
                console.log(res.status);
                this.error.value = "Unexpected HTTP status!";
                break;
            }
          })
          .catch(err => {
            console.log(err);
            this.error.value = "Connection error!";
          });
    },
    deleteTask(id) {
      if (confirm('Are you sure?')) {
        taskService.deleteTask(id)
            .then(res => {
              switch (res.status) {
                case HTTP_NO_CONTENT:
                  this._deleteTask(id);
                  break;
                case HTTP_UNAUTHORIZED:
                case HTTP_FORBIDDEN:
                  window.location.replace(authService.getAuthUrl());
                  break;
                default:
                  console.log(res.status);
                  this.error.value = "Unexpected HTTP status!";
                  break;
              }
            })
            .catch(err => {
              console.log(err);
              this.error.value = "Connection error!";
            });
      }
    },
    async toggleStatus(id) {
      const taskToggle = await this.fetchTask(id);
      const updateTask = {...taskToggle, status: !taskToggle.status};

      taskService.updateTaskStatus(updateTask.id, updateTask.text, updateTask.day, updateTask.status)
          .then(res => {
            switch (res.status) {
              case HTTP_OK:
                this._toggleStatus(res, id);
                break;
              case HTTP_UNAUTHORIZED:
              case HTTP_FORBIDDEN:
                window.location.replace(authService.getAuthUrl());
                break;
              default:
                console.log(res.status);
                this.error.value = "Unexpected HTTP status!";
                break;
            }
          })
          .catch(err => {
            console.log(err);
            this.error.value = "Connection error!";
          });
    },
    fetchTasks() {
      taskService.getTasks()
          .then(res => {
            switch (res.status) {
              case HTTP_OK:
                this.tasks = this._fetchTasks(res);
                break;
              case HTTP_UNAUTHORIZED:
              case HTTP_FORBIDDEN:
                window.location.replace(authService.getAuthUrl());
                break;
              default:
                console.log(res.status);
                this.error.value = "Unexpected HTTP status!";
                break;
            }
          })
          .catch(err => {
            console.log(err);
            this.error.value = "Connection error!";
          });
    },
    async fetchTask(id) {
      let data = {};

      await taskService.getTask(id)
          .then(res => {
            switch (res.status) {
              case HTTP_OK:
                data = this._fetchTask(res);
                break;
              case HTTP_UNAUTHORIZED:
              case HTTP_FORBIDDEN:
                window.location.replace(authService.getAuthUrl());
                break;
              default:
                console.log(res.status);
                this.error.value = "Unexpected HTTP status!";
                break;
            }
          })
          .catch(err => {
            console.log(err);
            this.error.value = "Connection error!";
          });

      return data;
    },
    _addTask(res) {
      const data = res.body;
      const newTask = {
        id: data.id,
        text: data.text,
        day: data.day,
        status: data.status
      }
      this.tasks = [...this.tasks, newTask];
    },
    _deleteTask(id) {
      this.tasks = this.tasks.filter((task) => task.id !== id)
    },
    _toggleStatus(res, id) {
      const data = res.body
      this.tasks = this.tasks.map((task) => task.id === id ? {...task, status: data.status} : task)
    },
    _fetchTasks(res) {
      let tasks = [];
      const data = res.body;
      if (data != null) {
        for (const task of data.tasks) {
          tasks.push({
            id: task.id,
            text: task.text,
            day: task.day,
            status: task.status
          });
        }
      }
      return tasks;
    },
    _fetchTask(res) {
      const data = res.body;
      return  {
        id: data.id,
        text: data.text,
        day: data.day,
        status: data.status
      }
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 30px auto;
  overflow: auto;
  min-height: 300px;
  border: 1px solid #2e4868;
  padding: 30px;
  border-radius: 5px;
  box-sizing: border-box;
}

.login-status {
  text-align: center;
  margin: 30px auto;
  }
</style>
