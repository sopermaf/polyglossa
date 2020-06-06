<template>
  <v-app-bar
    app
    class="banner"
    hide-on-scroll
  >
   
    <v-app-bar-nav-icon @click="openDrawer()"></v-app-bar-nav-icon>

    <!--<v-btn text @click="viewChoice('HOME')">
      <span class="mr-2">Home</span>
    </v-btn>

    <v-btn text @click="viewChoice('COURSES')" >
      <span class="mr-2">Courses</span>
    </v-btn>

    <v-btn text @click="viewChoice('BOOKING')">
      <span class="mr-2">Book a Class</span>
    </v-btn>
    -->
    <v-spacer></v-spacer>
    
    <v-toolbar-title class="headline text-uppercase">
      <span>Poly</span>
      <span class="font-weight-light">Glossa</span>
    </v-toolbar-title>

    
    <v-spacer></v-spacer>
    <!--
    <v-btn text  >
      <span class="mr-2">Exercises</span>
    </v-btn>

    <v-btn text  >
      <span class="mr-2">Texts</span>
    </v-btn>

    <v-btn text  >
      <span class="mr-2">Contact Us</span>
    </v-btn>
  -->
  </v-app-bar>
</template>

<script>
export default {
  name: "PolyToolbar",
  data: () => ({

  }),
  methods: {
    viewChoice(choice) {
      this.$emit("pageSelection", choice);
    },
    openDrawer() {
      console.log("called");
      this.$emit("drawer", true);
    }
  }
}
</script>


<style scoped>

</style>
