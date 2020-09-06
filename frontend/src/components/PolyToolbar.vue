<template>
  <v-app-bar
    app
    class="banner"
    color="#2f3253"
    prominent
  >

    <v-container>
      <v-layout row justify-center class="">
        <span
          class="d-flex-box-inline h1 mt-1"
        >
          <PolyGlossaTitle />
        </span>
      </v-layout>

      <v-layout row justify-center class="mb-4">
      <span
        class="d-flex-box-inline d-md-none"
      >
        <v-app-bar-nav-icon
          @click="openDrawer()"
        >
        </v-app-bar-nav-icon>
      </span>
      
      <span
        class="d-none d-md-flex"
        v-for="b in preLogoButtons" :key="b.export"
      >
        <v-btn
          text
          @click="viewChoice(b.export)"
          class="white--text"
        >
          <span class="mr-2">{{b.text}}</span>
        </v-btn>
      </span>

      <v-spacer></v-spacer>
      
      <v-spacer class=""></v-spacer>

      <span
        class="d-none d-md-flex"
        v-for="b in postLogoButtons" :key="b.export"
      >
        <v-btn
          text
          @click="viewChoice(b.export)"
          class="white--text"
        >
          <span class="mr-2">{{b.text}}</span>
        </v-btn>
      </span>
      </v-layout>
    </v-container>
  </v-app-bar>
</template>

<script>
import PolyGlossaTitle from "./PolyGlossaTitle";

export default {
  name: "PolyToolbar",
   components: {
    PolyGlossaTitle,
  },
  data: () => ({
    preLogoButtons: [
      {text: 'Home', export: 'HOME'},
      {text: 'Seminar Types', export: 'COURSES'},
      {text: 'Join a Seminar', export: 'BOOKING'},
    ],
    postLogoButtons: [
      {text: 'Learning Material', export: 'LEARNING'},
      {text: 'About Us', export: 'ABOUT_US'},
      {text: 'Contact Us', export: 'CONTACT_US'},
    ],
  }),
  methods: {
    viewChoice(choice) {
      this.$emit("pageSelection", choice);
    },
    openDrawer() {
      this.$emit("drawer", true);
    }
  }
}
</script>
