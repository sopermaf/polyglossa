<template>
  <v-app>
    <!-- Header -->
    <PolyToolbar />

    <!-- Page Content -->
    <v-content>
      <Home />
    </v-content>

    <!-- Footer -->
    <PolyFooter />

  </v-app>
</template>

<script>
import Home from './components/Home';
import PolyToolbar from './components/PolyToolbar.vue';
import PolyFooter from './components/PolyFooter.vue';

export default {
  name: 'Index',
  components: {
    Home,
    PolyToolbar,
    PolyFooter,
  },
  data: () => ({
    //
  }),
};
</script>
