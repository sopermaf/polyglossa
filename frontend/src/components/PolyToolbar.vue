<template>
  <v-app-bar
    app
    class="banner"
    hide-on-scroll
  >

    <template v-if="isNavBarVisible">
      <v-app-bar-nav-icon @click="openDrawer()"></v-app-bar-nav-icon>
    </template>
    <template v-else>
      <v-btn text @click="viewChoice('HOME')">
        <span class="mr-2">Home</span>
      </v-btn>

      <v-btn text @click="viewChoice('COURSES')" >
        <span class="mr-2">Courses</span>
      </v-btn>

      <v-btn text @click="viewChoice('BOOKING')">
        <span class="mr-2">Book a Class</span>
      </v-btn>
    </template>
    
    <v-spacer></v-spacer>
    
    <v-toolbar-title class="headline text-uppercase">
      <span>Poly</span>
      <span class="font-weight-light">Glossa</span>
    </v-toolbar-title>

    <v-spacer></v-spacer>

    <template v-if="!isNavBarVisible">    
      <v-btn text  >
        <span class="mr-2">Exercises</span>
      </v-btn>

      <v-btn text  >
        <span class="mr-2">Texts</span>
      </v-btn>

      <v-btn text  >
        <span class="mr-2">Contact Us</span>
      </v-btn>
    </template>
  </v-app-bar>
</template>

<script>
export default {
  name: "PolyToolbar",
  props: {
    isNavBarVisible: {
      type: Boolean
    }
  },
  data: () => ({
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
