<template>
  <v-container>
    <v-layout text-center justify-center wrap>
      <v-flex mb-5 xs12>
        <h1> Seminars </h1>
      </v-flex>


        <v-flex ma-3 lg6 md4 xs12 v-for="sem in classTypes" :key="sem">
          <v-card  outlined hover>
            <v-card-title class="justify-center mx-auto"> {{sem.title}} - ${{sem.price}} </v-card-title>
            <v-card-text> {{sem.description}} </v-card-text>
          </v-card>
        </v-flex>

    </v-layout>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data: () => ({
    classTypes: [],
  }),
  mounted() {
    axios.get('/book_class/get/activities/SEM').then(response => {
      this.classTypes = response.data['activities'];
      console.log(response);
    });
  }
};
</script>
