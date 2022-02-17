<template>
    <div class="center">
    <div class="item">
      <h4 class="center">New publication</h4>
      <textarea class="textboxid" placeholder="Make new publication" type="text" minlength=1 v-model="newPublication"></textarea><br>
      <button @click="addItem">post</button>
    </div>
    <br>
    
    <div class="item"
     v-for="item in items"
     v-bind:key="item.id">
     <div class="center">
      <div v-if="item.edit">
        <textarea class="textboxid" type="text" v-model="editPublication"></textarea><br>
      </div>
      <div v-else>
      <button class="right" v-if="!item.edit && !editing && item.owner === current" @click="editItem(item.id)">edit</button>
      <p class="left"> {{item.editDate}}</p> 
      

      <h3 class="center">{{item.owner}}</h3>
      <div class="left">
      <p class="multiline">{{item.publication}}</p>
      </div>
      </div>
      <button v-if="item.edit" @click="saveItem(item.id)">save</button>
      <button v-if="item.edit" @click="removeItem(item.id)">delete</button> 
      </div>
    </div>
    </div>
</template>

<script>
import {ref} from "vue";
import {publicationService} from "@/services/publication-service";
import {HTTP_201_CREATED, HTTP_FORBIDDEN, HTTP_NO_CONTENT, HTTP_OK, HTTP_UNAUTHORIZED} from "@/utils/http-status";
import {publicationValidators} from "@/utils/publication-validators";
import {authService} from "../services/auth-service";

export default {
  name: 'ThePublication',
  props: ['current'],
  created() {
    const error = ref("");
    publicationService.getPublications()
          .then(res => {
            switch (res.status) {
              case HTTP_OK:
                if(res.body != null) {
                  for (const publication of res.body.publications) {
                    this.items.push({
                      publication: publication.content,
                      owner: publication.owner,
                      edit: false,
                      editDate: publication.lastEdition,
                      id: publication.id
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
      owner: this.current,
      newPublication: '',
      editPublication: '',
      items: []
    }
  },
  methods: {
    addItem(){
      const error = ref("");
      error.value = publicationValidators.validatePublication(this.newPublication);
      if (error.value) {
        console.log(error)
        return error;
      }
      publicationService.addPublication(this.newPublication)
          .then(res => {
            switch (res.status) {
              case HTTP_201_CREATED:
                this._addItem(res)
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
    _addItem(res){
      this.items.push({
        publication: this.newPublication,
        owner: this.current,
        edit: false,
        editDate: res.body.lastEdition,
        id: res.body.id
        })
      this.newPublication = ''

    },
    removeItem(id){
      const error = ref("");
      publicationService.deletePublication(id)
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

    editItem(id){
      this.editing=true
      const index = this.items.findIndex(el => el.id === id)
      this.items[index].edit = true
      this.editPublication = this.items[index].publication
    },
    saveItem(id){
      const index = this.items.findIndex(el => el.id === id)

      if(this.items[index].publication !== this.editPublication)
      {
        const error = ref("");
        error.value = publicationValidators.validatePublication(this.editPublication);
        if (error.value) {
          console.log(error)
          return error;
        }
      publicationService.editPublication(id, this.editPublication)
          .then(res => {
            switch (res.status) {
              case HTTP_OK:
                this._editItem(id, index, res)
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
      }
    },
    _editItem(id, index, res){
      this.items.splice(index, 1,{
        publication: this.editPublication,
        owner: this.current,
        edit: false,
        editDate: res.body.lastEdition,
        id: id
        })
      this.editPublication = ''
      this.editing=false
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
      margin-left: 50px;
      margin-right: 50px;
      
  }
  .center{
      text-align: center;
  }
  .right{
      text-align: right;
      float: right;
      margin-right: 20px;
  }
  .item{
    border: 3px solid black;
    margin: 8px auto;
    margin-bottom: 1px;
    margin-top: 1px;
    padding: 1px;
    background-color: rgb(20, 126, 43);
    width: 500px;
  }
</style>
