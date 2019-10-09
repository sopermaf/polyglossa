<template>
  <v-app centered>
    <!-- Header -->
    <PolyToolbar />

    <!-- Page Content -->
    <v-content>
      <v-container fluid>
        <v-layout row wrap align-center>
          
          <v-flex md4 xs4></v-flex>
          
          <v-flex md4 xs4 >
            <BookClassForm/>
          </v-flex>
          
          <v-flex md4 xs4></v-flex>
        </v-layout>
      </v-container >
    </v-content>

    <!-- Footer -->
    <PolyFooter />

  </v-app>
</template>

<script>
import BookClassForm from './components/BookClassForm.vue';
import PolyToolbar from './components/PolyToolbar.vue';
import PolyFooter from './components/PolyFooter.vue';

export default {
  name: 'BookClass',
  components: {
    BookClassForm,
    PolyToolbar,
    PolyFooter,
  },
  data: () => ({
    //
  }),
};
</script>
