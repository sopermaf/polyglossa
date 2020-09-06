<template>
  <v-app-bar
    app
    class="banner"
    color="#2f3253"
    prominent
    absolute
  >

    <v-container>
      <v-layout row justify-center no-gutters class="">
        <v-app-bar-nav-icon
          class=" d-md-none"
          @click="openDrawer()"
          >
        </v-app-bar-nav-icon>
        
        <v-toolbar-title
          class="d-flex"
        >
          <PolyGlossaTitle />
        </v-toolbar-title>  
      </v-layout>

      <v-layout row justify-center no-gutters class="pb-5">
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
