<template>
  <v-app-bar
    app
    class="banner"
    color="#2f3253"
  >

    <template v-if="isNavBarVisible">
      <v-app-bar-nav-icon @click="openDrawer()"></v-app-bar-nav-icon>
    </template>
    <template v-else>
      <span v-for="b in preLogoButtons" :key="b.export">
        <v-btn
          text
          @click="viewChoice(b.export)"
          class="white--text"
        >
          <span class="mr-2">{{b.text}}</span>
        </v-btn>
      </span>
    </template>
    
    <v-spacer></v-spacer>
    
    <v-img
      :src="require('../assets/logo.png')"
      contain
      height="100%"
    ></v-img>

    <v-spacer></v-spacer>

    <template v-if="!isNavBarVisible">    
      <span v-for="b in postLogoButtons" :key="b.export">
        <v-btn
          text
          @click="viewChoice(b.export)"
          class="white--text"
        >
          <span class="mr-2">{{b.text}}</span>
        </v-btn>
      </span>
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
