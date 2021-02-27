<template>
  <v-app-bar
    app
    class="banner"
    color="#2f3253"
    absolute
  >

    <v-container>
      <template v-if="isSPAToolbar">
        <!-- Smaller Display Toolbar -->
        <v-layout
          row
          :class="`d-${switchPoint}-none d-flex justify--center`"
        >
          <v-app-bar-nav-icon
            class="mt-2"
            id="navBarIcon"
            @click="openDrawer()"
            >
          </v-app-bar-nav-icon>

          <v-spacer></v-spacer>

          <v-toolbar-title
            @click="viewChoice('HOME')"
          >
            <PolyGlossaTitle />
          </v-toolbar-title> 

          <v-spacer></v-spacer>
        </v-layout>

        <!-- Larger Display Toolbar -->
        <v-layout
          row
          justify-space-around
          no-gutters
          :class="`mb-1 d-none d-${switchPoint}-flex`"
        >
          <span
            class="d-flex"
            v-for="b in preLogoButtons" :key="b.export"
          >
            <v-btn
              text
              @click="viewChoice(b.export)"
              class="white--text mt-4"
            >
              <span class="mr-2">{{b.text}}</span>
            </v-btn>
          </span>

          <v-toolbar-title
            class="d-flex"
            @click="viewChoice('HOME')"
            to='/'
          >
            <PolyGlossaTitle />
          </v-toolbar-title> 

          <span
            class="d-flex"
            v-for="b in postLogoButtons" :key="b.export"
          >
            <v-btn
              text
              @click="viewChoice(b.export)"
              class="white--text mt-4"
            >
              <span class="mr-2">{{b.text}}</span>
            </v-btn>
          </span>
        </v-layout>
      </template>

      <!-- Non-Main Page Toolbar -->
      <template v-else>
        <v-layout
          row
          justify-space-around
          no-gutters
          :class="`mb-1 d-flex`"
        >

          <a href="/">
            <v-toolbar-title
              class="d-flex"
            >
              <PolyGlossaTitle />
            </v-toolbar-title>
          </a>
        </v-layout>
      </template>
    </v-container>
  </v-app-bar>
</template>

<script>
import PolyGlossaTitle from "./PolyGlossaTitle";

export default {
  name: "PolyToolbar",
  props: {
    switchPoint: {
      type: String,
      required: true,
    },
    isSPAToolbar: {
      type: Boolean,
      default: true
    }
  },
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


<style>

a {
    text-decoration: none;
}

#navBarIcon {
  background-color: #FFF176;
  border-radius: 30%;
}

</style>