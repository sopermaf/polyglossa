<template>
  <v-container>
    <v-layout text-center justify-center wrap>
      <v-flex mb-5 xs12>
        <h1> Seminar Descriptions </h1>
      </v-flex>


        <v-flex ma-3 lg6 md4 xs12 v-for="sem in classTypes" :key="sem">
          <v-card  outlined hover>
            <v-card-title class="justify-center mx-auto"> {{sem.title}} </v-card-title>

            <v-card-text> {{sem.description}} </v-card-text>
          </v-card>
        </v-flex>

    </v-layout>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    classTypes: [
      {
        title: 'Personalised Class',
        description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus a nulla molestie',
      },
      {
        title: 'Special English Class',
        description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus a nulla molestie',
      },
      {
        title: 'Third English Class',
        description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus a nulla molestie',
      },
    ],
  }),
  mounted() {
    // get the Seminar Activities
  }
};
</script>
