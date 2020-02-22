<template>
  <v-app>
    <!-- Header -->
    <PolyToolbar />

    <!-- Page Content -->
    <v-content>
      <template v-if="pageSelection == 'HOME'">
        <Home />
      </template>
      <template v-else-if="pageSelection == 'COURSES'">
        <Courses />
      </template>
    </v-content>

    <!-- Footer -->
    <PolyFooter />

  </v-app>
</template>

<script>
import Home from './components/Home';
import Courses from './components/Courses';
import PolyToolbar from './components/PolyToolbar.vue';
import PolyFooter from './components/PolyFooter.vue';

export default {
  name: 'Index',
  components: {
    Home,
    Courses,
    PolyToolbar,
    PolyFooter,
  },
  data: () => ({
    pageSelection: "HOME",
  }),
};
</script>
