<template>
  <v-container>
    <v-layout text-center justify-center wrap>

      <v-flex mb-5 xs12>
        <h1> Seminars </h1>
      </v-flex>

      <v-flex ma-3 lg6 md4 xs12 v-for="sem in classTypes" :key="sem">
        <CourseSlot :sem="sem" @courseChoice="openForm"/>
      </v-flex>


    </v-layout>
  </v-container>
</template>

<script>
import axios from "axios";
import CourseSlot from "./CourseSlot";

export default {
  components: {
    CourseSlot,
  },
  data: () => ({
    classTypes: [],
    courseChoice: null,
  }),
  mounted() {
    axios.get(process.env.VUE_APP_API_URL + '/book_class/get/activities/SEM').then(response => {
      this.classTypes = response.data['activities'];
    });
  },
  methods: {
    openForm(seminar) {
      this.$emit("courseChoice", seminar);
    }
  }
};
</script>
