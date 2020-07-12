<template>
  <v-container>
    <v-layout text-center wrap justify-center>
        <h1> Contact Us </h1>
        
        <div class="break" />

        <v-flex ma-5 lg7 s12 xs12>
            <p>
                For any inquiries, questions, or problems,
                please send an email to help@polyglossa.com.
            </p>
            <p>
                Alternatively check out our social media channels
                for more information or inquiries.
            </p>
        </v-flex>

        <div class="break" />

        <h1> Social Media </h1>

        <div class="break" />

        <v-flex ma-5 lg3 s3 xs3 v-for="social in socialMedia" :key="social.title">
            <v-card
                hover
                shaped
                :href="social.link"
            >
                <v-img
                    :src="social.image"
                    max-height="100"
                    contain
                />
                <v-card-title>
                    {{social.detail}}
                </v-card-title>
            </v-card>
        </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  props: {
      socialMedia: {
          type: Array,
          required: true,
      }
  },
  data: () => ({
    contactDetails: [
      {name: 'Email', data: 'example@polyglossa.com'},
    ],
  }),
};
</script>
