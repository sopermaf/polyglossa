<template>
  <v-app>
    <!-- Header -->
    <PolyToolbar />

    <!-- Page Content -->
    <v-content>
      <div>
        Class Booking Page
      </div>
    </v-content>

    <!-- Footer -->
    <PolyFooter />

  </v-app>
</template>

<script>
import PolyToolbar from './components/PolyToolbar.vue';
import PolyFooter from './components/PolyFooter.vue';

export default {
  name: 'BookClass',
  components: {
    PolyToolbar,
    PolyFooter,
  },
  data: () => ({
    //
  }),
};
</script>
