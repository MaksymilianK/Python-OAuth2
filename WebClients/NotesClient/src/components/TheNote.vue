<template>
    <div class="center">
    <div class="item">
      <h4 class="center">New note</h4>
      <input placeholder="title" type="text" minlength=1 v-model="newTitle" ><br>
      <textarea class="textboxid" placeholder="note" type="text" minlength=1 v-model="newNote"></textarea><br>
      <button @click="addItem(newTitle, newNote, 'newNote')">add</button>
    </div>
    <br>

    <div class="item"
     v-for="item in items"
     v-bind:key="item.id">
     <div class="center">
      <div v-if="item.edit">
        <input  type="text" v-model="editTitle" ><br>
        <textarea class="textboxid" type="text" v-model="editNote"></textarea><br>
      </div>
      <div v-else>
      <h5 class="right">last edit: {{item.editDate}}</h5>
      <h3>{{item.title}}</h3>
      <div class="left">
      <p class="multiline" v-if="item.show">{{item.note}}</p>
      
      </div>
      </div>
      <button v-if="!item.show && !item.edit" @click="showItem(item.id)">show</button>
      <button v-if="item.show && !item.edit" @click="hideItem(item.id)">hide</button>
      <button v-if="!item.edit && !editing" @click="editItem(item.id)">edit</button>
      <button v-if="item.edit" @click="saveItem(item.id, editTitle, editNote, 'editNote')">save</button>
      <button v-if="item.edit" @click="removeItem(item.id)">delete</button> 
    </div>
    </div>
  </div>
</template>

<script>
import {ref} from "vue";
import {noteValidators} from "@/utils/note-validators";
import {noteService} from "@/services/note-service";
import {
  HTTP_201_CREATED,
  HTTP_FORBIDDEN,
  HTTP_NO_CONTENT,
  HTTP_OK,
  HTTP_UNAUTHORIZED
} from "@/utils/http-status";
import {authService} from "../services/auth-service";

export default {
  name: 'TheNote',
  created() {
    const error = ref("");
    noteService.getNotes()
          .then(res => {
            switch (res.status) {
              case HTTP_OK:
                if(res.body != null) {
                  for (const note of res.body.notes) {
                    this.items.push({
                      title: note.title,
                      note: note.content,
                      show: false,
                      edit: false,
                      editDate: note.lastEdition,
                      id: note.id
                    })
                  }
                }
                break;
              case HTTP_UNAUTHORIZED:
              case HTTP_FORBIDDEN:
                window.location.replace(authService.getAuthUrl());
                break;
              default:
                error.value = "Unexpected error!";
                break;
            }
          })
          .catch(err => {
            console.log(err);
            error.value = "Connection error!";
          });

    return {
      error,
    }
  },
  data(){
    return{
      editing: false,
      newTitle: '',
      newNote: '',
      editTitle: '',
      editNote: '',
      items: [],
    }
  },
  methods: {
    addItem(noteTitle, noteContent, noteType){
      const error = ref("");
      const validators = noteValidators;
      error.value = validators.validateTitle(noteTitle);
      if (error.value) {
        console.log(error)
        return error;
      }
      error.value = validators.validateNote(noteContent);
      if (error.value) {
        console.log(error)
        return error;
      }
      noteService.addNote(noteTitle, noteContent)
          .then(res => {
            switch (res.status) {
              case HTTP_201_CREATED:
                this._addItem(noteTitle, noteContent, res, noteType)
                break;
              case HTTP_UNAUTHORIZED:
              case HTTP_FORBIDDEN:
                window.location.replace(authService.getAuthUrl());
                break;
              default:
                error.value = "Unexpected error!";
                break;
            }
          })
          .catch(err => {
            console.log(err);
            error.value = "Connection error!";
          });
      return null
    },
    _addItem(noteTitle, noteContent, res, noteType){
      this.items.push({
        title: noteTitle,
        note: noteContent,
        show: false,
        edit: false,
        editDate: res.body.lastEdition,
        id: res.body.id
        })

      if(noteType === 'editNote') {
        this.editTitle = ''
        this.editNote = ''
      }
      else{
        this.newTitle = ''
        this.newNote = ''
      }
    },
    removeItem(id){
      const error = ref("");
      noteService.deleteNote(id)
          .then(res => {
            switch (res.status) {
              case HTTP_NO_CONTENT:
                this._removeItem(id)
                break;
              case HTTP_UNAUTHORIZED:
              case HTTP_FORBIDDEN:
                window.location.replace(authService.getAuthUrl());
                break;
              default:
                error.value = "Unexpected error!";
                break;
            }
          })
          .catch(err => {
            console.log(err);
            error.value = "Connection error!";
          });
    },
    _removeItem(id){
      const index = this.items.findIndex(el => el.id === id)
      if (this.items[index].edit)
      {this.editing = false}
      this.items.splice(index, 1)
    },
    showItem(id){
      const index = this.items.findIndex(el => el.id === id)
      this.items[index].show = true
    },
    hideItem(id){
      const index = this.items.findIndex(el => el.id === id)
      this.items[index].show = false
    },
    editItem(id){
      this.editing=true
      const index = this.items.findIndex(el => el.id === id)
      this.items[index].edit = true
      this.editTitle = this.items[index].title
      this.editNote = this.items[index].note
    },
    saveItem(id, noteTitle, noteContent){
      const index = this.items.findIndex(el => el.id === id)

      if(this.items[index].title !== this.editTitle ||
      this.items[index].note !== this.editNote)
      {
        if (this.addItem(noteTitle, noteContent) === null){
          this.removeItem(id)
          this.editing = false
        }
      }
    }
  }
}
</script>

<style scoped>
  .textboxid{
      height: 150px;
      width: 400px;
  }
  .multiline {
  white-space: pre-wrap;
  }
  .left{
      text-align: left;
  }
  .center{
      text-align: center;
  }
  .right{
      text-align: right;
  }
  .item{
    border: 3px solid black;
    margin: 8px auto;
    padding: 1px;
    background-color: rgb(71, 207, 231);
    width: 500px;
  }
</style>
