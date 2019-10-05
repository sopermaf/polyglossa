<template>
  <v-app>
    <!-- Header -->
    <PolyToolbar />

    <!-- Page Content -->
    <v-content>
      <div>
        <BookClassMain />
      </div>
    </v-content>

    <!-- Footer -->
    <PolyFooter />

  </v-app>
</template>

<script>
import BookClassMain from './components/BookClassMain.vue';
import PolyToolbar from './components/PolyToolbar.vue';
import PolyFooter from './components/PolyFooter.vue';

export default {
  name: 'BookClass',
  components: {
    BookClassMain,
    PolyToolbar,
    PolyFooter,
  },
  data: () => ({
    //
  }),
};
</script>
