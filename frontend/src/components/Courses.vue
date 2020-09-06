<template>
  <v-container>
    <v-layout text-center justify-center wrap>

      <v-flex mb-5 xs12>
        <h1> Seminars </h1>
      </v-flex>

      <v-flex ma-3 lg6 md4 xs12 v-for="sem in seminars" :key="sem">
        <CourseSlot :sem="sem" @courseChoice="openForm"/>
      </v-flex>

    </v-layout>
  </v-container>
</template>

<script>
import CourseSlot from "./CourseSlot";

export default {
  components: {
    CourseSlot,
  },
  props: {
    seminars: {
      type: Array,
      required: true,
    }
  },
  data: () => ({
    courseChoice: null,
  }),
  methods: {
    openForm(seminar) {
      this.$emit("courseChoice", seminar);
    }
  }
};
</script>
